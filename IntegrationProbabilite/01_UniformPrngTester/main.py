import random as rd
import math


class UniformDistributionExperiment:
    """
    An environment for the random.uniform function distribution test
    ...
    Attributes
    ----------
    lower_bound : float
        The lowest value possibly returned by the random function
    upper_bound : float
        The highest value possibly returned by the random function
    draw_nb : int
        The number of random values drawn within the experience (default 10,000)
    subdivision_nb : int
        The number of intervals of equal length within the interval [lower_bound, upper_bound) (default 10)

    Methods
    -------
    start()
        Starts the experiment
    compile()
        Compiles various data about the experience, such as mean, standard deviation, etc.
    get_expected_mean()
        Returns the expected mean of the theoretical uniform distribution
    get_expected_std()
        Returns the standard deviation of the theoretical uniform distribution
    """

    DRAW_NB = 10_000
    SUBDIVISION_NB = 10

    def __init__(self, lower_bound: float, upper_bound: float, draw_nb: int = DRAW_NB,
                 subdivision_nb: int = SUBDIVISION_NB):
        """
        Parameters
        ----------
        lower_bound : float
            the lowest value possibly returned by the random function
        upper_bound : float
            the highest value possibly returned by the random function
        draw_nb : int
            the number of random values drawn within the experience (default 10,000)
        subdivision_nb : int
            the number of intervals of equal length within the interval [lower_bound, upper_bound) (default 10)

        Raises
        ------
        ValueError
            If any of the three conditions below is met, a Value Error is raised :
            * `lower_bound` is higher or equal than `upper_bound`
            * `draw_nb` is fewer than 1
            * `subdivision_nb` is fewer than 1
        """

        if lower_bound >= upper_bound:
            raise ValueError('Lower bound should be strictly lower than upper bound.')
        if draw_nb < 1:
            raise ValueError('Draw number should be an integer, and at least 1.')
        if subdivision_nb < 1:
            raise ValueError('Subdivision number should be an integer, and at least 1.')

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.draw_number = draw_nb
        self.subdivision_nb = subdivision_nb

        self.cups = [0] * subdivision_nb

        self.mean = -1
        self.std = -1

    def __str__(self):
        return "Interval : [%s,%s) | Number of subdivisions : %s | Number of draws : %s" \
               % (self.lower_bound, self.upper_bound, self.subdivision_nb, self.draw_number)

    def start(self) -> None:
        """
        Draws `draw_number` numbers uniformly between `lower_bound` and `upper_bound`, and counts where this number
        lies within the `subdivision_nb` different intervals.
        """

        for _ in range(self.draw_number):
            x = rd.uniform(self.lower_bound, self.upper_bound)  # Draw a random number uniformly within [lb,ub)
            cup_id = math.floor(x * self.subdivision_nb)  # Find correct cup associated to the random number
            self.cups[cup_id] += 1

        self.__compile()

    def __compile(self) -> None:
        """
        (internal) Compiles various data about the experience, such as mean, standard deviation, etc.
        """

        self.__calculate_mean()
        self.__calculate_std()
        pass

    def __calculate_mean(self) -> None:
        """
        (internal) Calculates the mean of the distribution
        """

        mean = 0.0
        for i in range(self.subdivision_nb):
            avg_x = (2*i + 1)/2/self.subdivision_nb + self.lower_bound
            mean += avg_x * self.cups[i]

        self.mean = mean/self.draw_number

    def __calculate_std(self) -> None:
        """
        (internal) Calculates the standard deviation of the distribution
        """
        var = 0.0
        for i in range(self.subdivision_nb):
            avg_x = (2 * i + 1) / 2 / self.subdivision_nb + self.lower_bound
            var += (self.cups[i]/self.draw_number * avg_x**2)

        self.std = math.sqrt(var - self.mean**2)

    def get_expected_mean(self) -> float:
        """
        Calculates the expected mean of the distribution
        """
        return (self.lower_bound + self.upper_bound)/2

    def get_expected_std(self) -> float:
        """
        Calculates the expected standard deviation of the distribution
        """
        return math.sqrt((self.upper_bound - self.lower_bound)**2 / 12)


exp = UniformDistributionExperiment(lower_bound=0, upper_bound=1, draw_nb=10_000, subdivision_nb=10)
exp.start()
print(exp)
print("Mean : {:.4} (expected {:.4} | error : {:.4%})".format(
    exp.mean, exp.get_expected_mean(), (exp.mean-exp.get_expected_mean())/exp.mean))
print("Standard deviation : {:.4} (expected {:.4} | error : {:.4%})".format(
    exp.std, exp.get_expected_std(), (exp.std-exp.get_expected_std())/exp.std))
