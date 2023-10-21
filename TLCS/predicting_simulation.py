import traci
import numpy as np
import random
import timeit
import os

# phase codes based on environment.net.xml
PHASE_NS_GREEN = 0  # action 0 code 00
PHASE_NS_YELLOW = 1
PHASE_NSL_GREEN = 2  # action 1 code 01
PHASE_NSL_YELLOW = 3
PHASE_EW_GREEN = 4  # action 2 code 10
PHASE_EW_YELLOW = 5
PHASE_EWL_GREEN = 6  # action 3 code 11
PHASE_EWL_YELLOW = 7

# envr2, 24603 for seed 1000 w/ bus & truck; envr3, 28000 for seed 1000 w/ bus & truck
# need to pass in flow and waiting queue

class Simulation:
    def __init__(self, Model, max_steps, green_duration, yellow_duration, num_states, num_actions, lanes):
        self._Model = Model
        #self._TrafficGen = TrafficGen
        self._step = 0
        #self._sumo_cmd = sumo_cmd
        self._max_steps = max_steps
        self._green_duration = green_duration
        self._yellow_duration = yellow_duration
        self._num_states = num_states
        self._num_actions = num_actions
        self._reward_episode = []
        self._queue_length_episode = []
        self._last_waiting = []
        self._steps_left = 0
        self._waiting_times = {}
        self._old_action = -1
        self._old_flow = 0
        self._current_flow = 0
        self._lanes = lanes
        self._isyellow = False
        self._action = -1


    def run(self, car_queue):
        """
        Runs the testing simulation
        """
        print(car_queue.N_Straight._car, car_queue.S_Straight._car, car_queue.W_Straight._car, car_queue.E_Straight._car, car_queue.N_Turn._car, car_queue.S_Turn._car, car_queue.W_Turn._car, car_queue.E_Turn._car)
        # start_time = timeit.default_timer()

        # first, generate the route file for this simulation and set up sumo
        #self._TrafficGen.generate_routefile(seed=episode)
        #traci.start(self._sumo_cmd)
        #print("Simulating...")

        # inits
        #self._step = 0
        #self._waiting_times = {}
        #old_total_wait = 0
        #old_action = -1 # dummy init

        #old_flow=0
        #current_flow=0

        if self._step < self._max_steps:
            if self._steps_left > 0:
                self._steps_left -= 1
                self._step += 1
                return 0
            # get current state of the intersection
            if not self._isyellow:
                current_state, self._current_flow = self._get_state(self._old_action, car_queue)


            # idea: use prev action to see 車流量 in moving lane and combine with waiting lane's number
            # to create state.


            # calculate reward of previous action: (change in cumulative waiting time between actions)
            # waiting time = seconds waited by a car since the spawn in the environment, cumulated for every car in incoming lanes
            #current_total_wait = self._collect_waiting_times()
            #reward = old_total_wait - current_total_wait

            # choose the light phase to activate, based on the current state of the intersection
                self._action = self._choose_action(current_state, self._current_flow, self._old_flow, self._old_action, car_queue)

            # if the chosen phase is different from the last phase, activate the yellow phase
                if self._step != 0 and self._old_action != self._action:
                    self._set_yellow_phase(self._old_action)
                    self._simulate(self._yellow_duration)
                    self._isyellow = True
                    return 0

            # execute the phase selected before
            if self._isyellow:
                self._isyellow = False
            self._set_green_phase(self._action)
            self._simulate(self._green_duration)

            # saving variables for later & accumulate reward
            self._old_action = self._action
            #old_total_wait = current_total_wait
            self._old_flow = self._current_flow
            self._step += 1

            #self._reward_episode.append(reward)

        #print("Total reward:", np.sum(self._reward_episode))
        # car_list = traci.vehicle.getIDList()
        # total_waiting_time=0
        # for car_id in car_list:
        #     wait_time = traci.vehicle.getAccumulatedWaitingTime(car_id)
        #     total_waiting_time += wait_time
        # traci.close()
        #simulation_time = round(timeit.default_timer() - start_time, 1)


        return 0 #simulation_time


    def _simulate(self, steps_todo):
        """
        Proceed with the simulation in sumo
        """
        if (self._step + steps_todo) >= self._max_steps:  # do not do more steps than the maximum allowed number of steps
            steps_todo = self._max_steps - self._step

        self._steps_left = steps_todo
        # while steps_todo > 0:
            # traci.simulationStep()  # simulate 1 step in sumo
            # self._step += 1 # update the step counter
            # steps_todo -= 1
            #queue_length = self._get_queue_length() 
            #queue_length = self._collect_waiting_times() 
            #self._queue_length_episode.append(queue_length)


    # def _collect_waiting_times(self):
    #     """
    #     Retrieve the waiting time of every car in the incoming roads
    #     """
    #     incoming_roads = ["E2TL", "N2TL", "W2TL", "S2TL"]
    #     car_list = traci.vehicle.getIDList()
    #     for car_id in car_list:
    #         wait_time = traci.vehicle.getAccumulatedWaitingTime(car_id)
    #         road_id = traci.vehicle.getRoadID(car_id)  # get the road id where the car is located
    #         if road_id in incoming_roads:  # consider only the waiting times of cars in incoming roads
    #             self._waiting_times[car_id] = wait_time
    #         else:
    #             if car_id in self._waiting_times: # a car that was tracked has cleared the intersection
    #                 del self._waiting_times[car_id] 
    #                 self._last_waiting.append(wait_time)
    #     total_waiting_time = sum(self._waiting_times.values())
    #     return total_waiting_time


    def _choose_action(self, state, current_flow, old_flow, old_action, car_queue):
        """
        Pick the best action known based on the current state of the env
        """
        if old_action != 1:
            NS_turn_queue= car_queue.N_Turn._total + car_queue.S_Turn._total  #traci.lane.getLastStepHaltingNumber("N2TL_2") + traci.lane.getLastStepHaltingNumber("S2TL_2")
        else:
            NS_turn_queue = 0
        if old_action != 3:
            WE_turn_queue=  car_queue.W_Turn._total + car_queue.E_Turn._total #traci.lane.getLastStepHaltingNumber("W2TL_2") + traci.lane.getLastStepHaltingNumber("E2TL_2")
        else:
            WE_turn_queue = 0
        if old_action != 0:
            NS_straight_queue= car_queue.N_Straight._total + car_queue.S_Straight._total   #traci.edge.getLastStepHaltingNumber("N2TL") + traci.edge.getLastStepHaltingNumber("S2TL") - NS_turn_queue
        else:
            NS_straight_queue = 0
        if old_action != 2:
            WE_straight_queue=  car_queue.W_Straight._total + car_queue.E_Straight._total  #traci.edge.getLastStepHaltingNumber("E2TL") + traci.edge.getLastStepHaltingNumber("W2TL") - WE_turn_queue
        else:
            WE_straight_queue = 0

        total_queue = NS_straight_queue + NS_turn_queue + WE_straight_queue + WE_turn_queue

        if current_flow < 3 and old_flow < 3:
            if old_action == 1 or old_action == 3:
                if current_flow < 1 and old_flow < 1 and total_queue < 5 and total_queue > 0:
                    if old_action == 1:
                        if NS_straight_queue > WE_straight_queue + WE_turn_queue:
                            return 0
                        else:
                            if WE_straight_queue > WE_turn_queue:
                                return 2
                            else:
                                return 3
                    else:
                        if WE_straight_queue > NS_straight_queue + NS_turn_queue:
                            return 2
                        else:
                            if NS_straight_queue > NS_turn_queue:
                                return 0
                            else:
                                return 1
                else:
                    return np.argmax(self._Model.predict_one(state))
            else:
                if total_queue < 5 and total_queue > 0:
                    if old_action == 0:
                        return 2
                    else:
                        return 0
                else:
                    return np.argmax(self._Model.predict_one(state))
        else:
            return np.argmax(self._Model.predict_one(state))


    def _set_yellow_phase(self, old_action):
        """
        Activate the correct yellow light combination in sumo
        """
        #yellow_phase_code = old_action * 2 + 1 # obtain the yellow phase code, based on the old action (ref on environment.net.xml)
        #traci.trafficlight.setPhase("TL", yellow_phase_code)

        # need to output yellow light signal
        if old_action == 0:
            print("NS_Straight_Yellow")
        elif old_action == 1:
            print("NS_Turn_Yellow")
        elif old_action == 2:
            print("WE_Straight_Yellow")
        elif old_action == 3:
            print("WE_Turn_Yellow")


    def _set_green_phase(self, action_number):
        """
        Activate the correct green light combination in sumo
        """


        if action_number == 0:
            #traci.trafficlight.setPhase("TL", PHASE_NS_GREEN)
            print("NS_Straight_Green")
        elif action_number == 1:
            print("NS_Turn_Green")
            #traci.trafficlight.setPhase("TL", PHASE_NSL_GREEN)
        elif action_number == 2:
            print("WE_Straight_Green")
            #traci.trafficlight.setPhase("TL", PHASE_EW_GREEN)
        elif action_number == 3:
            print("WE_Trun_Green")
            #traci.trafficlight.setPhase("TL", PHASE_EWL_GREEN)


    # def _get_queue_length(self, car_queue, ):
    #     """
    #     Retrieve the number of cars with speed = 0 in every incoming lane
    #     """
    #     halt_N = traci.edge.getLastStepHaltingNumber("N2TL")
    #     halt_S = traci.edge.getLastStepHaltingNumber("S2TL")
    #     halt_E = traci.edge.getLastStepHaltingNumber("E2TL")
    #     halt_W = traci.edge.getLastStepHaltingNumber("W2TL")
    #     queue_length = halt_N + halt_S + halt_E + halt_W

    #     return queue_length


    def _get_state(self,old_action, car_queue):
        """
        Retrieve the state of the intersection from sumo, in the form of cell occupancy
        """
        state = np.zeros(self._num_states)
        #car_list = traci.vehicle.getIDList()
        lane_car = np.zeros(16)

        # for car_id in car_list:
        #     lane_pos = traci.vehicle.getLanePosition(car_id)
        #     lane_id = traci.vehicle.getLaneID(car_id)
        #     lane_pos = 750 - lane_pos  # inversion of lane pos, so if the car is close to the traffic light -> lane_pos = 0 --- 750 = max len of a road

            
            # distance in meters from the traffic light -> mapping into cells
            # if lane_pos < 7:
            #     lane_cell = 0
            # elif lane_pos < 14:
            #     lane_cell = 1
            # elif lane_pos < 21:
            #     lane_cell = 2
            # elif lane_pos < 28:
            #     lane_cell = 3
            # elif lane_pos < 40:
            #     lane_cell = 4
            # elif lane_pos < 60:
            #     lane_cell = 5
            # elif lane_pos < 100:
            #     lane_cell = 6
            # elif lane_pos < 160:
            #     lane_cell = 7
            # elif lane_pos < 400:
            #     lane_cell = 8
            # elif lane_pos <= 750:
            # #     lane_cell = 9
            # if lane_pos < 0:
            #     lane_cell = 9
            # elif lane_pos < 7:
            #     lane_cell = 0
            # elif lane_pos < 14:
            #     lane_cell = 1
            # elif lane_pos < 21:
            #     lane_cell = 2
            # elif lane_pos < 28:
            #     lane_cell = 3
            # elif lane_pos < 35:
            #     lane_cell = 4
            # elif lane_pos < 45:
            #     lane_cell = 5
            # elif lane_pos < 55:
            #     lane_cell = 6
            # elif lane_pos < 65:
            #     lane_cell = 7
            # elif lane_pos < 80:
            #     lane_cell = 8
            # elif lane_pos <= 750:
            #     lane_cell = 9

            # finding the lane where the car is located 
            # x2TL_3 are the "turn left only" lanes
            # if lane_id == "W2TL_0" or lane_id == "W2TL_1" or lane_id == "W2TL_2":
            #     lane_group = 0
            # elif lane_id == "W2TL_3":
            #     lane_group = 1
            # elif lane_id == "N2TL_0" or lane_id == "N2TL_1" or lane_id == "N2TL_2":
            #     lane_group = 2
            # elif lane_id == "N2TL_3":
            #     lane_group = 3
            # elif lane_id == "E2TL_0" or lane_id == "E2TL_1" or lane_id == "E2TL_2":
            #     lane_group = 4
            # elif lane_id == "E2TL_3":
            #     lane_group = 5
            # elif lane_id == "S2TL_0" or lane_id == "S2TL_1" or lane_id == "S2TL_2":
            #     lane_group = 6
            # elif lane_id == "S2TL_3":
            #     lane_group = 7
            # else:
            #     lane_group = -1

            # if lane_group >= 1 and lane_group <= 7:
            #     car_position = int(str(lane_group) + str(lane_cell))  # composition of the two postion ID to create a number in interval 0-79
            #     valid_car = True
            # elif lane_group == 0:
            #     car_position = lane_cell
            #     valid_car = True
            # else:
            #     valid_car = False  # flag for not detecting cars crossing the intersection or driving away from it

            # if valid_car:
            #     state[car_position] = 1  # write the position of the car car_id in the state array in the form of "cell occupied"

        # for car_id in car_queue:
        #     car_type = 0
        #     car_vclass = car_id.vclass
        #     if car_vclass == "car" or car_vclass == "truck":
        #         car_type = 1
        #     else:
        #         car_type = 0

        #     if car_id.lane == "W_Straight":
        #         if lane_car[0] + car_type < 10:
        #             lane_car[0] += 1
        #     elif car_id.lane == "W_Turn":
        #         if lane_car[1] + car_type < 5:
        #             lane_car[1] += 1
        #     elif car_id.lane == "N_Straight":
        #         if lane_car[2] + car_type < 10:
        #             lane_car[2] += 1
        #     elif car_id.lane == "N_Turn":
        #         if lane_car[3] + car_type < 5:
        #             lane_car[3] += 1
        #     elif car_id.lane == "E_Straight":
        #         if lane_car[4] + car_type < 10:
        #             lane_car[4] += 1
        #     elif car_id.lane == "E_Turn":
        #         if lane_car[5] + car_type < 5:
        #             lane_car[5] += 1
        #     elif car_id.lane == "S_Straight":
        #         if lane_car[6] + car_type < 10:
        #             lane_car[6] += 1
        #     elif car_id.lane == "S_Turn":
        #         if lane_car[7] + car_type < 5:
        #             lane_car[7] += 1
        if self._lanes == 3:
            lane_car[0] = car_queue.W_Straight._car + car_queue.W_Straight._bus*2 + car_queue.W_Straight._truck*1.5
            if lane_car[0] >= 10:
                lane_car[0] = 10
            lane_car[1] = car_queue.W_Turn._car + car_queue.W_Turn._bus*2 + car_queue.W_Turn._truck*1.5
            if lane_car[1] >= 5:
                lane_car[1] = 5
            lane_car[2] = car_queue.N_Straight._car + car_queue.N_Straight._bus*2 + car_queue.N_Straight._truck*1.5
            if lane_car[2] >= 10:
                lane_car[2] = 10
            lane_car[3] = car_queue.N_Turn._car + car_queue.N_Turn._bus*2 + car_queue.N_Turn._truck*1.5
            if lane_car[3] >= 5:
                lane_car[3] = 5
            lane_car[4] = car_queue.E_Straight._car + car_queue.E_Straight._bus*2 + car_queue.E_Straight._truck*1.5
            if lane_car[4] >= 10:
                lane_car[4] = 10
            lane_car[5] = car_queue.E_Turn._car + car_queue.E_Turn._bus*2 + car_queue.E_Turn._truck*1.5
            if lane_car[5] >= 5:
                lane_car[5] = 5
            lane_car[6] = car_queue.S_Straight._car + car_queue.S_Straight._bus*2 + car_queue.S_Straight._truck*1.5
            if lane_car[6] >= 10:
                lane_car[6] = 10
            lane_car[7] = car_queue.S_Turn._car + car_queue.S_Turn._bus*2 + car_queue.S_Turn._truck*1.5
            if lane_car[7] >= 5:
                lane_car[7] = 5
        else:
            lane_car[0] = car_queue.W_Straight._car + car_queue.W_Straight._bus*2 + car_queue.W_Straight._truck*1.5
            if lane_car[0] >= 15:
                lane_car[0] = 15
            lane_car[1] = car_queue.W_Turn._car + car_queue.W_Turn._bus*2 + car_queue.W_Turn._truck*1.5
            if lane_car[1] >= 5:
                lane_car[1] = 5
            lane_car[2] = car_queue.N_Straight._car + car_queue.N_Straight._bus*2 + car_queue.N_Straight._truck*1.5
            if lane_car[2] >= 15:
                lane_car[2] = 15
            lane_car[3] = car_queue.N_Turn._car + car_queue.N_Turn._bus*2 + car_queue.N_Turn._truck*1.5
            if lane_car[3] >= 5:
                lane_car[3] = 5
            lane_car[4] = car_queue.E_Straight._car + car_queue.E_Straight._bus*2 + car_queue.E_Straight._truck*1.5
            if lane_car[4] >= 15:
                lane_car[4] = 15
            lane_car[5] = car_queue.E_Turn._car + car_queue.E_Turn._bus*2 + car_queue.E_Turn._truck*1.5
            if lane_car[5] >= 5:
                lane_car[5] = 5
            lane_car[6] = car_queue.S_Straight._car + car_queue.S_Straight._bus*2 + car_queue.S_Straight._truck*1.5
            if lane_car[6] >= 15:
                lane_car[6] = 15
            lane_car[7] = car_queue.S_Turn._car + car_queue.S_Turn._bus*2 + car_queue.S_Turn._truck*1.5
            if lane_car[7] >= 5:
                lane_car[7] = 5
        
        flow_count=0
        total_flow=0
        if old_action==0:
            flow_count = lane_car[2] + lane_car[6]
            lane_car[2]=0; lane_car[6] = 0
            state[8] = flow_count
            total_flow += flow_count
        if old_action==1:
            flow_count = lane_car[3] + lane_car[7]
            lane_car[3]=0; lane_car[7]=0
            state[9] = flow_count
            total_flow += flow_count
        if old_action==2:
            flow_count = lane_car[0] + lane_car[4]
            lane_car[0]=0; lane_car[4]=0
            state[10] = flow_count
            total_flow += flow_count
        if old_action==3:
            flow_count = lane_car[1] + lane_car[5]
            lane_car[1]=0; lane_car[5]=0
            state[11] = flow_count
            total_flow += flow_count

        if self._lanes == 3:
            for i in range(8):
                total_s = 0
                if i%2==0:
                    for j in range(int(lane_car[i])):
                        total_s += -(j+1)*(j+1)*(j+1)*0.006 + 20
                else:
                    total_s = lane_car[i]
                state[i] = total_s
        else:
            for i in range(8):
                total_s = 0
                if i%2==0:
                    for j in range(int(lane_car[i])):
                        total_s += -(j+1)*(j+1)*(j+1)*0.006 + 20
                else:
                    total_s = lane_car[i]
                state[i] = total_s


        return state, total_flow


    @property
    def queue_length_episode(self):
        return self._queue_length_episode


    @property
    def reward_episode(self):
        return self._reward_episode



