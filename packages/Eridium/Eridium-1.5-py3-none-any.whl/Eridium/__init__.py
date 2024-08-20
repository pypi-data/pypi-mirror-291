class Eridium:
    def print(self, number):
        if not isinstance(number, int) or number < 0:
            raise ValueError("Число должно быть неотрицательным целым числом")
        result = 1
        for i in range(1, number + 1):
            result *= i
        print(result)

    def sqrt_print(self, number):
        if not isinstance(number, (int, float)) or number < 0:
            raise ValueError("Число должно быть неотрицательным")
        x = number
        y = (x + 1) / 2
        while abs(y - x) > 1e-10:
            x = y
            y = (x + number / x) / 2
        print(y)

    def quint_func(self, number):
        if not isinstance(number, (int, float)):
            raise ValueError("Число должно быть числом")
        result = number ** 5
        print(result)

    def natural_log(self, number):
        if not isinstance(number, (int, float)) or number <= 0:
            raise ValueError("Число должно быть положительным")
        x = number - 1
        result = 0
        for i in range(1, 10000):
            result += ((-1) ** (i + 1)) * (x ** i) / i
        return result

    def natural_log_print(self, number):
        result = self.natural_log(number)
        print(result)

    def binary_log_print(self, number):
        if not isinstance(number, (int, float)) or number <= 0:
            raise ValueError("Число должно быть положительным")
        natural_log = self.natural_log(number)
        binary_log = natural_log / self.natural_log(2)
        print(binary_log)

    def sigma_func(self, number):
        if not isinstance(number, int) or number < 1:
            raise ValueError("Число должно быть положительным целым числом")
        result = 0
        for i in range(1, number + 1):
            if number % i == 0:
                result += i
        print(result)

fact = Eridium()
quint = Eridium()
natural_log = Eridium()
binary_log = Eridium()
sigma = Eridium()
