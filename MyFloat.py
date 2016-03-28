MAXDEC_MAN = 0b1111111
MINDEC_MAN = 0b1000000
MIN_MAN = 0.5
MAX_MAN = 0.9999999

def Standardize(un_stand_float):
    tmp_man = int(un_stand_float.mantissa, 2)
    if tmp_man == 0:
        raise Exception("ERROR. Result is Zero.")
    tmp_exp = (-1)**un_stand_float.sign_exp * int(un_stand_float.exponent, 2)
    result = MyFloat()
    result.sign_man = un_stand_float.sign_man
    if tmp_man < MINDEC_MAN:
        while tmp_man < MINDEC_MAN:
            tmp_man *= 2
            tmp_exp -= 1
    elif tmp_man > MAXDEC_MAN:
        while tmp_man > MAXDEC_MAN:
            tmp_man //= 2
            tmp_exp += 1
    result.mantissa = bin(tmp_man)[2:]
    if tmp_exp >= 0:
        result.sign_exp = 0
    else:
        result.sign_exp = 1
    tmp_exp = bin(abs(tmp_exp))[2:]
    while len(tmp_exp) < 7:
        tmp_exp = '0' + tmp_exp
    result.exponent = tmp_exp
    return result

def Trans_to_16_bit(origin_float):
    if origin_float > 0:
        sign_man = 0
    else:
        sign_man = 1
    origin_float = abs(origin_float)
    if origin_float >= MIN_MAN and origin_float < MAX_MAN:
        sign_exp = 1
        exponent = '0000000'
    if origin_float < MIN_MAN:
        n = 0
        while origin_float < MIN_MAN:
            origin_float = origin_float * 2
            n = n - 1           
        sign_exp = 1
        exponent = Trans_to_exponent(n)
    if origin_float >= MAX_MAN:
        n = 0
        while origin_float >= MAX_MAN:
            origin_float = origin_float / 2
            n = n + 1           
        sign_exp = 0
        exponent = Trans_to_exponent(n)
    mantissa = Trans_to_mantissa(origin_float)
    return [sign_exp, exponent, sign_man, mantissa]

def Trans_to_origin(binary_float):
    a = binary_float
    origin_float = 2**((-1)**a.sign_exp * int(a.exponent, 2)) * (-1)**a.sign_man * int(a.mantissa, 2) / 128.0
    return origin_float

def Trans_to_mantissa(man_of_float):
    tmp = []
    while len(tmp) < 7:
        tmp.append(int(man_of_float*2))
        man_of_float = man_of_float*2 - tmp[-1]
    mantissa = ''.join([str(i) for i in tmp])
    if mantissa == '0000000':
        raise Exception("ERROR. Number is out of range.")
    return mantissa

def Trans_to_exponent(n):
    exponent = bin(abs(n))[2:]
    if len(exponent) > 7:
        raise Exception("ERROR. Number is out of range.")
    while len(exponent) < 7:
        exponent = '0' + exponent
    return exponent

class MyFloat:
    def __init__(self, origin_float = 1.0):
        if type(origin_float) == 'str':
            raise Exception("ERROR. Input is not float number.")
        if origin_float == 0.0:
            raise Exception("ERROR. Zero is not allowed.")
        binary_float = Trans_to_16_bit(float(origin_float))
        self.sign_exp = binary_float[0]
        self.exponent = binary_float[1]
        self.sign_man = binary_float[2]
        self.mantissa = binary_float[3]
    
    def __str__(self):
        return 'Float result: ' + str(Trans_to_origin(self)) + '\n' \
               + 'MyFloat result: ' + str(self.sign_exp) + '_' + self.exponent + '_' + str(self.sign_man) + '_' + self.mantissa
        
    def __add__(self, hand):
        x = self
        y = hand
        result = MyFloat()
        if ((-1)**x.sign_exp * int(x.exponent, 2) < (-1)**y.sign_exp * int(y.exponent, 2)):
            small = x
            big = y
        else:
            small = y
            big = x
        result.sign_exp = big.sign_exp
        result.exponent = big.exponent
        se = (-1)**small.sign_exp * int(small.exponent, 2)
        be = (-1)**big.sign_exp * int(big.exponent, 2)
        sm = (-1)**small.sign_man * int(small.mantissa, 2)
        bm = (-1)**big.sign_man * int(big.mantissa, 2)
        tmp = (sm >> (be - se)) + bm
        if tmp < 0:
            result.sign_man = 1
        else:
            result.sign_man = 0
        result.mantissa = bin(abs(tmp))[2:] 
        result = Standardize(result)
        return result

    def __sub__(self, hand):
        x = self
        y = hand
        result = MyFloat()
        if ((-1)**x.sign_exp * int(x.exponent, 2) < (-1)**y.sign_exp * int(y.exponent, 2)):
            small = x
            big = y
            big.sign_man = 1 - y.sign_man
        else:
            small = y
            big = x
            small.sign_man = 1 - y.sign_man
        result.sign_exp = big.sign_exp
        result.exponent = big.exponent
        se = (-1)**small.sign_exp * int(small.exponent, 2)
        be = (-1)**big.sign_exp * int(big.exponent, 2)
        sm = (-1)**small.sign_man * int(small.mantissa, 2)
        bm = (-1)**big.sign_man * int(big.mantissa, 2)
        tmp = (sm >> (be - se)) + bm
        if tmp < 0:
            result.sign_man = 1
        else:
            result.sign_man = 0
        result.mantissa = bin(abs(tmp))[2:]
        result = Standardize(result)
        return result

    def __mul__(self, hand):
        a = self
        b = hand
        result = MyFloat()
        ae = int(a.exponent, 2)
        be = int(b.exponent, 2)
        am = int(a.mantissa, 2)
        bm = int(b.mantissa, 2)
        if(a.sign_exp == b.sign_exp):
            result.sign_exp = a.sign_exp
            result.exponent = bin(ae + be)[2:]
        else:
            if(ae > be):
                result.sign_exp = a.sign_exp
                result.exponent = bin(ae - be)[2:]
            else:
                result.sign_exp = b.sign_exp
                result.exponent = bin(be - ae)[2:]
        tmp = bin(am * bm)[2:]
        if tmp[-8] == '0' and tmp[-7] == '1':
            result.mantissa = tmp[:-8] + '1'
        else:
            result.mantissa = tmp[:-7]
        if(a.sign_man == b.sign_man):
            result.sign_man = 0
        else:
            result.sign_man = 1
        result = Standardize(result)
        return result

    def __truediv__(self, hand):
        a = self
        b = hand
        result = MyFloat()
        ae = int(a.exponent, 2)
        be = int(b.exponent, 2)
        am = int(a.mantissa, 2)
        bm = int(b.mantissa, 2)
        if a.sign_exp == b.sign_exp :
            if ae > be :
                result.sign_exp = a.sign_exp
                result.exponent = bin(ae - be)[2:]
            else:
                result.sign_exp = 1 - b.sign_exp
                result.exponent = bin(be - ae)[2:]
        else:
            result.sign_exp = a.sign_exp
            result.exponent = bin(ae + be)[2:]
        tmp = 0
        i = 7
        remainder = am
        while i > 0 and remainder > 0:
            quotient = remainder // bm
            tmp += (quotient << i)
            remainder = remainder % bm
            remainder = remainder << 1
            i -= 1
        result.mantissa = bin(abs(am // bm) + tmp)[2:10]
        if(a.sign_man == b.sign_man):
            result.sign_man = 0
        else:
            result.sign_man =1
        result = Standardize(result)
        return result

def main(a, b):
    add = MyFloat(a) + MyFloat(b)
    sub = MyFloat(a) - MyFloat(b)
    mul = MyFloat(a) * MyFloat(b)
    div = MyFloat(a) / MyFloat(b)
    print ('\nadd:' + '\nSystem result: ' + str(a + b))
    print (add)
    print ('\nsub:' + '\nSystem result: ' + str(a - b))
    print (sub)
    print ('\nmul:' + '\nSystem result: ' + str(a * b))
    print (mul)
    print ('\ndiv:' + '\nSystem result: ' + str(a / b))
    print (div)

if __name__ == '__main__':
    import sys
    main(float(sys.argv[1]), float(sys.argv[2]))


'''
def fmtPrint(c, res):
    template = "%s,%f,%f,%f"
    print  template % (c, c.decode(), res, abs((res - c.decode()) / res))
    
def main(x, y):
    a = MyFloat(x)
    b = MyFloat(y)
    c = a + b
    fmtPrint(c, x + y)
    c = a - b
    fmtPrint(c, x - y)
    c = a * b
    fmtPrint(c, x * y)
    c = a / b
    fmtPrint(c, x / y)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print ('Usage:\npython ' + sys.argv[0] + ' float1 float2')
        sys.exit(1)
    
    main(float(sys.argv[1]), float(sys.argv[2]))
'''
