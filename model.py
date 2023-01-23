import mesa


class Person(mesa.Agent):
    # TODO
    smoking_severity = 1
    response_efficacy = 1

    def __init__(self, unique_id: int, model: mesa.Model, hedonism: float, security: float, security_feeling: float,
                 conformity: float, smoking_attitude: float, vulnerability: float):
        super().__init__(unique_id, model)
        # desires between [0,1]; TODO maybe add thresholds for each desire (water tank model)
        self.hedonism = hedonism
        self.security = security
        self.security_feeling = security_feeling
        self.conformity = conformity
        self.smoking_attitude = smoking_attitude
        self.vulnerability = vulnerability
        # tolerance level determines if an agent stays connected with another agent
        # could differ for each agent (dict)
        self.tolerance_levels = dict()
        # list with agents in social group of agent
        self.social_group = list()  # TODO

    def step(self):
        # deciding what to do: adaptive or maladaptive response
        # calculate social pressure (separately for social group and of local environment)
        # print(self.calc_social_pressure(True))
        # if tolerance_level < threshold then cut bonds with agent
        print("STEP")
        print(self.tolerance_levels)
        print(self.social_group)
        # print(self.model.schedule.agents)

    # TODO balance adaptive/maladaptive response
    def calc_adaptive_resp(self):
        # (RE + SE) - ((conformity * part of SP thats against own interest) + hedonism)
        # Self efficacy goes down with decisions against own interest; stronger when SP is stronger)
        pass

    def calc_maladaptive_resp(self):
        # (hedonism + smoking_attitude) - (severity_discount + personal_vulnerability)
        pass

    def calc_social_pressure(self, static: bool):
        """
        # TODO Gewichtung local/social pressure in Literatur nachschauen
        Calculates the social pressure based on the social group of the agent.
        :param static: determines if whole population or only social group is used to calculate the social pressure
        :return: average smoking attitude of agents in social group / population
        """
        sum_smoking_attitude = 0
        if static:
            for agent in self.model.schedule.agents:
                sum_smoking_attitude += agent.smoking_attitude
            return sum_smoking_attitude
        else:
            for agent in self.social_group:
                sum_smoking_attitude += agent.smoking_attitude
        return sum_smoking_attitude

    def calc_local_pressure(self):
        """
        Calculates the local social pressure by determining the average smoking attitude in the neighborhood.
        :return: average smoking attitude of neighboring agents
        """
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        local_agents = list()
        for pos in neighborhood:
            neighbors = self.model.grid.get_cell_list_contents([pos])
            for agent in neighbors:
                local_agents.append(agent)
        sum_smoking_attitude = 0
        for agent in local_agents:
            sum_smoking_attitude += agent.smoking_attitude
        return sum_smoking_attitude


class SocialPressureModel(mesa.Model):
    """A model with some number of agents."""
    def __init__(self, N: int, width: int, height: int):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        # Create agents
        # Create agents
        for i in range(self.num_agents):
            person = Person(i,
                            self,
                            self.random.uniform(0, 1),
                            self.random.uniform(0, 1),
                            self.random.uniform(0, 1),
                            self.random.uniform(0, 1),
                            self.random.uniform(0, 1),
                            self.random.uniform(0, 1))
            self.schedule.add(person)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(person, (x, y))
        # create (social) links between agents (this will only work if every agent is Person)
        for person in self.schedule.agents:
            number_of_friends = self.random.randint(1, 5)  # this could be a parameter
            friends = self.random.choices(self.schedule.agents, k=number_of_friends)
            for friend in friends:
                person.social_group.append(friend)
                person.tolerance_levels[friend] = self.random.uniform(0.8, 1)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
