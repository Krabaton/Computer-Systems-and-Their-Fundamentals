def mul(a, b):
    return a * b


def async_mul(a, b, callback):
    result = a * b
    callback(result)


if __name__ == "__main__":
    result = mul(2, 3)
    print(result)
    async_mul(2, 3, print)
