import random

numbers = set()
while len(numbers) < 3:
    numbers.add(str(random.randint(0, 9)))
numbers = list(numbers)

print("*" * 60)
print("야구게임을 시작합니다.")
print("*" * 60)

count_strike = 0
count_ball = 0

while count_strike < 3:
    num = input("숫자 3자리를 입력하세요: ")
    if len(num) == 3:
        for i in range(3):
            if num[i] == numbers[i]:
                count_strike += 1
            elif num[i] in numbers:
                count_ball += 1
        if count_strike == 0 and count_ball == 0:
            print("3 아웃!!")
        else:
            output = []
            if count_strike > 0:
                output.append("{} 스트라이크".format(count_strike))
            if count_ball > 0:
                output.append("{} 볼".format(count_ball))
            print(" ".join(output))

print("게임 성공")
