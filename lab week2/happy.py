#
# 생일 축하 함수
#
def say_happy_birthday(name:str) -> None:
    print("안녕하세요")
    print(name + "님의 생일을 축하합니다")
    return None

def test_happy_bitrhday():
    say_happy_birthday("권순욱")
    say_happy_birthday("정혜승")
    say_happy_birthday("조하늘")
    say_happy_birthday("김준서")

def test_happy_birthday2():
    names = ["순욱", "혜승", "하늘", "준서"]
    for name in names:
        say_happy_birthday(name)

def test_happy_birthday3():
    say_happy_birthday(3.14159)
    # say_happy_birthday(100)
    # say_happy_birthday([1,2,3])

if __name__ == "_main_":
# test _happy_birthday()
# test _happy_birthday2()
    test_happy_birthday3()    