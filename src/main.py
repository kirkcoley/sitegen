from textnode import TextType, TextNode

def main():
    print("hello nurse")
    node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(repr(node))

main()
