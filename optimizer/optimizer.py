from backtesting.optimizer.parameter_grid import (
    generate_parameter_grid
)


def main():

    parameters = generate_parameter_grid()

    print("=" * 60)

    print("AI Trading Bot Optimizer")

    print("=" * 60)

    print()

    print("Total Parameter Sets :", len(parameters))

    print()

    print("First 10 Combinations")

    print()

    for parameter in parameters[:10]:

        print(parameter)


if __name__ == "__main__":

    main()