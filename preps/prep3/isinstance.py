class F:
    def __init__(self) -> None:
        pass

class G(F):
    # Implementation Omitted
    pass

class H(G):
    # Implementation Omitted
    pass

if __name__ == '__main__':
    f = F()
    g = G()
    h = H()
    
    print(isinstance(h,F))