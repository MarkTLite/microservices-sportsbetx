print("========== Definition ==========")
def make_bold(fn):
    print("make_bold decorator")
    def wrapper():
        print("bold")
        return "<b>" + fn() + "</b>"
    return wrapper

def make_italic(fn):
    print("make_italic decorator")
    def wrapper():
        print("italic")
        return "<i>" + fn() + "</i>"
    return wrapper

@make_bold
@make_italic
def hello():
  return "hello world"

print("\n========== Execution ==========")
print(hello())