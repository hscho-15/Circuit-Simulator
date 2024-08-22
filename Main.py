# Circuit Simulator #
# Made by hscho-15 #
# v0.0.1-alpha #
# Compiled: 2024. 06. 15. #

# Main.py
from References import * # References.py 로딩하기

# pygame 시작!
pygame.init()

# pygame 창 띄우기
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# 유용한 변수 선언하기
running : bool = True # 게임 실행 여부 저장
selected_component : Component = None # 선택한 구성 요소 저장
dragging_node : Node = None # 현재 만드는 전선의 첫번째 시작 연결점 저장
offset_x : int = 0 # 선택한 부분이 구성 요소의 어느 부분인지 저장 (x좌표)
offset_y : int = 0 # 선택한 부분이 구성 요소의 어느 부분인지 저장 (y좌표)
new_component : Component = None # 새로운 구성 요소 저장

# 회로 생성
circuit = Circuit()

# pygame 메인 반복문
while running:
    for event in pygame.event.get():

        # 창 닫는 이벤트
        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭 이벤트
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # 마우스 왼쪽 클릭.
            if event.button == 1:
                # 새 구성 요소 생성 후 배치할 때
                if new_component != None:
                    selected_component = None
                    moving = False
                    new_component = None

                # 구성 요소에 클릭 -> 움직이기 시작
                for component in circuit.components:
                    if component.rect.collidepoint(event.pos):
                        selected_component = component
                        offset_x = component.rect.x - event.pos[0]
                        offset_y = component.rect.y - event.pos[1]
                        break

                # 구성요소 새로 추가하는 버튼 클릭 -> 구성 요소 추가하기
                if event.pos[1] > height - 100:

                    # 배터리 추가 버튼
                    if event.pos[0] <= 200:

                        # 유저가 제대로 입력할 때 까지 반복
                        while True:
                            # 베터리 전압 입력받기
                            user_input = simpledialog.askstring("전압 입력", "배터리의 전압을 V 단위로 입력하세요. 취소하려면 아무 것도 입력하지 마세요:")

                            # 암것도 입력 안 한 경우 -> 실수로 버튼 누른것으로 판단해 입력 취소
                            if not user_input:
                                user_input_bool = False
                                break

                            # 숫자 입력한 경우 -> 제대로 입력했으므로 while 반복문 빠져나오기
                            if user_input.isnumeric():
                                user_input_bool = True
                                break

                            # 이상한거 입력한 경우
                            else:
                                # 오류 메세지
                                messagebox.showinfo("전압 입력", "숫자만 입력해 주세요!")

                        # 입력했는 경우 -> 배터리 객체 생성
                        if user_input_bool == True:
                            v = int(user_input)
                            n1 = Node("N{0}".format(len(circuit.nodes)), event.pos)
                            n2 = Node("N{0}".format(len(circuit.nodes)+1), (event.pos[0] + 25, event.pos[1] + 25))
                            circuit.add_node(n1)
                            circuit.add_node(n2)
                            new_component = Battery("B{0}".format(len(list(filter(lambda x: isinstance(x, Battery), circuit.components)))), v, event.pos, n1, n2)
                            selected_component = new_component
                            circuit.add_component(new_component)


                    # 저항 추가 버튼
                    elif event.pos[0] <= 400:

                        # 유저가 제대로 입력할 때 까지 반복
                        while True:
                            # 저항 저항값 입력받기
                            user_input = simpledialog.askstring("저항값 입력",
                                                                "저항의 저항값을 Ω 단위로 입력하세요. 취소하려면 아무 것도 입력하지 마세요:")

                            # 암것도 입력 안 한 경우 -> 실수로 객체 생성 버튼 누른것으로 판단해 입력 취소
                            if not user_input:
                                user_input_bool = False
                                break

                            # 숫자 입력한 경우 -> 제대로 입력했으므로 while 반복문 빠져나오기
                            if user_input.isnumeric():
                                user_input_bool = True
                                break

                            # 이상한거 입력한 경우
                            else:
                                # 오류 메세지
                                messagebox.showinfo("저항값 입력", "숫자만 입력해 주세요!")

                        # 입력했는 경우 -> 배터리 객체 생성
                        if user_input_bool == True:
                            r = int(user_input)
                            n1 = Node("N{0}".format(len(circuit.nodes)), event.pos)
                            n2 = Node("N{0}".format(len(circuit.nodes) + 1), (event.pos[0] + 25, event.pos[1] + 25))
                            circuit.add_node(n1)
                            circuit.add_node(n2)
                            new_component = Resistor(
                                "R{0}".format(len(list(filter(lambda x: isinstance(x, Resistor), circuit.components)))),
                                r, event.pos, n1, n2)
                            selected_component = new_component
                            circuit.add_component(new_component)

                    # LED 추가 버튼
                    elif event.pos[0] <= 600:

                        # 유저가 제대로 입력할 때 까지 반복
                        while True:
                            # LED 저항값 입력받기
                            user_input = simpledialog.askstring("저항값 입력",
                                                                "LED의 저항값을 Ω 단위로 입력하세요. 취소하려면 아무 것도 입력하지 마세요:")

                            # 암것도 입력 안 한 경우 -> 실수로 객체 생성 버튼 누른것으로 판단해 입력 취소
                            if not user_input:
                                user_input_bool = False
                                break

                            # 숫자 입력한 경우 -> 제대로 입력했으므로 while 반복문 빠져나오기
                            if user_input.isnumeric():
                                user_input_bool = True
                                break

                            # 이상한거 입력한 경우
                            else:
                                # 오류 메세지
                                messagebox.showinfo("저항값 입력", "숫자만 입력해 주세요!")

                        # 입력했는 경우 -> 배터리 객체 생성
                        if user_input_bool == True:
                            r = int(user_input)
                            n1 = Node("N{0}".format(len(circuit.nodes)), event.pos)
                            n2 = Node("N{0}".format(len(circuit.nodes) + 1), (event.pos[0] + 25, event.pos[1] + 25))
                            circuit.add_node(n1)
                            circuit.add_node(n2)
                            new_component = LED(
                                "L{0}".format(len(list(filter(lambda x: isinstance(x, LED), circuit.components)))),
                                r, event.pos, n1, n2)
                            selected_component = new_component
                            circuit.add_component(new_component)

                    # 시뮬레이션 버튼
                    else:
                        circuit.solve()

            # 마우스 오른쪽 클릭
            elif event.button == 3:
                # 우클릭한 연결점 찾기
                for component in circuit.components:
                    # node1이 연결됐는지 찾기
                    if component.node1.rect.collidepoint(event.pos):
                        dragging_node = component.node1
                        break

                    # node2가 연결됐는지 찾기
                    if component.node2.rect.collidepoint(event.pos):
                        dragging_node = component.node2
                        break

        # 마우스 클릭 떼는 이벤트
        elif event.type == pygame.MOUSEBUTTONUP:
            # 마우스 좌클릭 뗌
            if event.button == 1:
                # 새 구성 요소 생성 후 배치할 때를 제외하기
                if new_component == None:
                    selected_component = None
                    moving = False
                    new_component = None

            # 마우스 우클릭 뗌
            elif event.button == 3:
                # 전선 생성 도중이면 -> 마우스 위치에 다른 연결점이 있으면 전선 생성
                if dragging_node != None:
                    for component in circuit.components:
                        if component.node1.rect.collidepoint(event.pos):
                            if component.node1 != dragging_node:
                                circuit.add_wire(Wire(dragging_node, component.node1), component.node1, dragging_node)
                                break

                        if component.node2.rect.collidepoint(event.pos):
                            if component.node2 != dragging_node:
                                circuit.add_wire(Wire(dragging_node, component.node2), component.node2, dragging_node)
                                break


                    dragging_node = None

        # 마우스 움직이는 이벤트
        elif event.type == pygame.MOUSEMOTION:
            if selected_component != None:
                selected_component.rect.x = event.pos[0] + offset_x
                selected_component.rect.y = event.pos[1] + offset_y
                selected_component.node1.position = (selected_component.rect.x-10, selected_component.rect.y + selected_component.rect.height // 2)
                selected_component.node2.position = (selected_component.rect.x + selected_component.rect.width, selected_component.rect.y + selected_component.rect.height // 2)

    # 화면 하얗게 채우기
    screen.fill((255, 255, 255))

    # 버튼 생성
    pygame.draw.rect(screen, (0, 255, 0), (0, 500, 200, 100))
    pygame.draw.rect(screen, (251, 206, 177), (200, 500, 200, 100))
    pygame.draw.rect(screen, (255, 255, 0), (400, 500, 200, 100))
    pygame.draw.rect(screen, (0, 0, 0), (600, 500, 200, 100))

    # 버튼에 글자 새기기
    font1 = pygame.font.SysFont('malgungothicsemilight', 30)
    img1 = font1.render('배터리', True, (0, 0, 0))
    screen.blit(img1, (60, 525))

    img1 = font1.render('저항', True, (0, 0, 0))
    screen.blit(img1, (260, 525))

    img1 = font1.render('LED', True, (0, 0, 0))
    screen.blit(img1, (460, 525))

    img1 = font1.render('시뮬레이션', True, (255, 255, 255))
    screen.blit(img1, (630, 525))

    # 회로 그리기
    circuit.draw(screen)

    # 화면 수정 사항 반영
    pygame.display.flip()


# 게임 종료
pygame.quit()
sys.exit()
