# Main.py
import pygame
import numpy as np
from numpy.linalg import LinAlgError
from scipy.linalg import solve
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys


# 회로 총괄 클래스
class Circuit:
    # 회로 객체 생성자
    def __init__(self):
        self.components = []
        self.nodes = []
        self.wire_indices = {}
        self.wires = []

    # 회로에 구성 요소를 등록하는 메소드
    def add_component(self, component):
        self.components.append(component)
        component.node1.connected_components.append(component)
        component.node2.connected_components.append(component)


    # 회로에 구성 요소를 삭제하는 메소드
    def remove_component(self, component):
        self.components.remove(component)

    # 회로에 전선을 등록하는 메소드
    def add_node(self, node):
        self.nodes.append(node)

    def add_wire(self, wire, nodea, nodeb):
        self.wires.append(wire)
        nodea.connected_wires.append(wire)
        nodeb.connected_wires.append(wire)

    # 회로의 전류를 계산하는 메소드
    def solve(self):
        try:
            # 전선 인덱스 초기화
            self.wire_indices = {wire: i for i, wire in enumerate(self.wires)}
            num_wires = len(self.wires)
            A = np.zeros((num_wires, num_wires))
            b = np.zeros(num_wires)

            # 전선에 대한 방정식 설정
            for component in self.components:
                node1 = component.node1
                node2 = component.node2
                if isinstance(component, Resistor):
                    for wire in node1.connected_wires:
                        i = self.wire_indices[wire]
                        for wire2 in node2.connected_wires:
                            j = self.wire_indices[wire2]
                            A[i, i] += 1 / component.resistance
                            A[j, j] += 1 / component.resistance
                            A[i, j] -= 1 / component.resistance
                            A[j, i] -= 1 / component.resistance
                elif isinstance(component, LED):
                    for wire in node1.connected_wires:
                        i = self.wire_indices[wire]
                        for wire2 in node2.connected_wires:
                            j = self.wire_indices[wire2]
                            A[i, i] += 1 / component.resistance
                            A[j, j] += 1 / component.resistance
                            A[i, j] -= 1 / component.resistance
                            A[j, i] -= 1 / component.resistance
                elif isinstance(component, Battery):
                    for wire in node1.connected_wires:
                        i = self.wire_indices[wire]
                        for wire2 in node2.connected_wires:
                            j = self.wire_indices[wire2]
                            A[i, i] += 1e9
                            A[j, j] += 1e9
                            A[i, j] -= 1e9
                            A[j, i] -= 1e9
                            b[i] += component.voltage * 1e9
                            b[j] -= component.voltage * 1e9

            # 첫 번째 전선을 그라운드로 설정
            A[0, :] = 0
            A[:, 0] = 0
            A[0, 0] = 1
            b[0] = 0

            # 행렬 방정식 풀이
            potentials = solve(A, b)

            # 각 전선에 계산된 전압 설정
            for wire, i in self.wire_indices.items():
                wire.voltage = potentials[i]

            # 각 노드에 대해 전압 설정
            for node in self.nodes:
                node.potential = sum(wire.voltage for wire in node.connected_wires) / len(node.connected_wires)

            # 각 구성 요소에 대해 전류 계산
            for component in self.components:
                if isinstance(component, Resistor):
                    component.voltage = component.node1.potential - component.node2.potential
                    component.current = component.voltage / component.resistance
                elif isinstance(component, LED):
                    component.voltage = component.node1.potential - component.node2.potential
                    component.current = component.voltage / component.resistance
                elif isinstance(component, Battery):
                    component.voltage = component.voltage
                    component.current = (component.node1.potential - component.node2.potential) / component.voltage
                print("{0}: {1:.2}".format(component.name, component.current))

        except Exception as e:
            print("풀 수 없는 회로입니다. 모든 구성요소가 잘 연결되었는지 확인해 주세요.")
            print(f"에러 코드: {e}")
            return

    # 회로의 구성 요소, 전선 등을 그려주는 메소드
    def draw(self, screen):
        for component in self.components:
            component.draw(screen)
        for node in self.nodes:
            node.draw(screen)
        for wire in self.wires:
            wire.draw(screen)

# 전선 연결점 클래스
class Node:
    # 연결점 객체 생성자
    def __init__(self, name, position):
        self.name = name
        self.rect = pygame.Rect(position[0], position[1], 10, 10)
        self.position = position
        self.potential = 0.0
        self.connected_wires = []
        self.connected_components = []

    # 전선 그려주는 메소드
    def draw(self, screen):
        self.rect = pygame.Rect(self.position[0], self.position[1], 10, 10)
        pygame.draw.ellipse(screen, (0,0,255), self.rect)

# 전선 클래스
class Wire:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.voltage = 0.0

    def draw(self, screen):
        pygame.draw.line(screen, (0,0,0), self.start_node.position, self.end_node.position, 2)


# 구성 요소 클래스
# 구성 요소 총괄 클래스
class Component:
    # 구성 요소 객체 생성자
    def __init__(self, name: str, position: tuple, node1: Node, node2: Node):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 60, 20)
        self.node1 = node1
        self.node2 = node2
        self.current = 0.0

    # 구성 요소 그려주는 메소드
    def draw(self, screen):
        pass # 자식 클래스에서 정의할꺼에요!

# 배터리
class Battery(Component):
    # 배터리 객체 생성자
    def __init__(self, name: str, voltage: int, position: tuple, node1: Node, node2: Node):
        # Component 부모 클래스의 생성자 호출하기!
        super().__init__(name, position, node1, node2)

        # 전압 (self.voltage) 설정
        self.voltage = voltage

        # self.img, self.rect 설정
        img = pygame.image.load("./Images/battery.png") # 이미지 로드
        img = pygame.transform.scale(img, (56, 25)) # 이미지 크기 조정
        self.img = img
        self.rect = img.get_rect() # 이미지의 Rect 개체 로딩하기~
        self.rect.center = position[0]+28, position[1]+12.5 # Rect 개체의 중심을 설정

    # 배터리 그려주는 메소드
    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y)) # 이미지 표시하기


# 저항
class Resistor(Component):
    # 배터리 객체 생성자
    def __init__(self, name: str, resistance: int, position: tuple, node1: Node, node2: Node):
        # Component 부모 클래스의 생성자 호출하기!
        super().__init__(name, position, node1, node2)

        # 저항 (self.resistance) 설정
        self.resistance = resistance

        # self.img, self.rect 설정
        img = pygame.image.load("./Images/resistor.png")  # 이미지 로드
        img = pygame.transform.scale(img, (27, 12))  # 이미지 크기 조정
        self.img = img
        self.rect = img.get_rect()  # 이미지의 Rect 개체 로딩하기~
        self.rect.center = position[0] + 13.5, position[1] + 6  # Rect 개체의 중심을 설정

    # 배터리 그려주는 메소드
    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))  # 이미지 표시하기

        font1 = pygame.font.SysFont(None, 30)
        img1 = font1.render('{0:.2}A'.format(self.current), True, (0, 0, 0))
        screen.blit(img1, (self.rect.x, self.rect.y + 20))

# LED
class LED(Component):
    # 배터리 객체 생성자
    def __init__(self, name: str, resistance: int, position: tuple, node1: Node, node2: Node):
        # Component 부모 클래스의 생성자 호출하기!
        super().__init__(name, position, node1, node2)

        # 저항 (self.resistance) 설정
        self.resistance = resistance

        # self.img, self.rect 설정
        if self.current:
            img = pygame.image.load("Images/led_on.png")  # 이미지 로드
        else:
            img = pygame.image.load("Images/led_off.png")  # 이미지 로드
        img = pygame.transform.scale(img, (30, 35))  # 이미지 크기 조정
        self.img = img
        self.rect = img.get_rect()  # 이미지의 Rect 개체 로딩하기~
        self.rect.center = position[0] + 15, position[1] + 17.5  # Rect 개체의 중심을 설정

    # 배터리 그려주는 메소드
    def draw(self, screen):

        # self.img, self.rect 설정
        if self.current:
            img = pygame.image.load("Images/led_on.png")  # 이미지 로드
        else:
            img = pygame.image.load("Images/led_off.png")  # 이미지 로드
        img = pygame.transform.scale(img, (30, 35))  # 이미지 크기 조정
        self.img = img
        screen.blit(self.img, (self.rect.x, self.rect.y))  # 이미지 표시하기

        font1 = pygame.font.SysFont(None, 30)
        img1 = font1.render('{0:.2}A'.format(self.current), True, (0,0,0))
        screen.blit(img1, (self.rect.x, self.rect.y + 30))
