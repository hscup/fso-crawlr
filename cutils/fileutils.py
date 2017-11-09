def readlines(filename):
    content = ''
    with open(filename, mode='r') as f:
        content = f.read().splitlines()
        content = [line.strip() for line in content]
    
    return content
