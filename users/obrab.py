import easyocr

def text_recognition(filename):
    reader = easyocr.Reader(["ru", "en"])
    result = reader.readtext(filename, detail = 0)
    return result

def main():
    file = "011.jpg"
    print(text_recognition(file))
    
if __name__ == "__main__":
    main()