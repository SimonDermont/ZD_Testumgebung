import numpy as np

MOVEMENT_RULES = {"Rast":0,"v. const.":1,"Poly 5":2,"poly 5 connector":3}

class Section():

    def __init__(self, start_time, end_time, start_pos, end_pos, position_in_curve, bewegungsgesetz, zyklus, auflosung):
        self.t_s = start_time
        self.t_e = end_time
        self.p_s = start_pos
        self.p_e = end_pos
        self.pos = position_in_curve
        self.rule = bewegungsgesetz
        self.cycle = zyklus
        self.scale = auflosung

        self.data_ammount = 2 * self.scale*self.cycle+1

        self.t_data = np.linspace(0,self.cycle*2,num=self.data_ammount) # 360 hardcode - 14400 hardcode
        self.distance = self.p_e - self.p_s

        self.info = "I am {} with Ts={}, Te={}, s={} and {}".format(self.pos, self.t_s, self.t_e, self.distance, self.rule)

        print(self.info) #debuging statement

    def update_section_info(self):
        self.distance = self.p_e - self.p_s
        self.info = "I am {} with Ts={}, Te={}, s={} and {}".format(self.pos, self.t_s, self.t_e, self.distance, self.rule)

    def calc_pause(self):
        self.p_data = np.full(self.data_ammount,self.p_s) # 14400 hardcode
        self.v_data = np.full(self.data_ammount,0) # 14400 hardcode
        self.a_data = np.full(self.data_ammount,0) # 14400 hardcode

    def calc_vconst(self):
        if self.t_s > self.t_e:
            t_e_calc = self.t_e + self.cycle
        else:
            t_e_calc = self.t_e
            
        velocity = (self.p_e - self.p_s)/(t_e_calc - self.t_s)
        coef = self.p_s - velocity * self.t_s
        self.p_data = coef + velocity * self.t_data
        self.v_data = np.full(self.data_ammount,velocity) # 14400 hardcode
        self.a_data = np.full(self.data_ammount,0) # 14400 hardcode

    def calc_poly(self, v_s = 0, a_s = 0, v_e = 0, a_e = 0, wp = 0.5):
        print("calc poly with p0:{} v0:{} a0:{} p1:{} v1:{} a1:{}".format (self.p_s,v_s,a_s,self.p_e,v_e,a_e))

        if self.t_s > self.t_e:
            t_e_calc = self.t_e + self.cycle
        else:
            t_e_calc = self.t_e

        b = np.array([self.p_s, v_s, a_s, self.p_e, v_e, a_e])
        Arr = np.zeros([0,6])

        for x in [self.t_s, t_e_calc]:
            p_solve = np.polynomial.Polynomial([1, x, x**2, x**3, x**4, x**5])
            v_solve = np.polynomial.Polynomial([0, 1, 2*x, 3*x**2, 4*x**3, 5*x**4])
            a_solve = np.polynomial.Polynomial([0, 0, 2, 6*x, 12*x**2, 20*x**3])

            row_n = Arr.shape[0] ##last row
            Arr = np.insert(Arr,row_n,[p_solve.coef],axis= 0)
            Arr = np.insert(Arr,row_n+1,[v_solve.coef],axis= 0)
            Arr = np.insert(Arr,row_n+2,[a_solve.coef],axis= 0)

        coefficients = np.linalg.solve(Arr,b)
        #coefficients_rounded = coefficients.round(decimals=3)

        p = np.polynomial.Polynomial(coefficients)
        v = p.deriv()
        a = p.deriv(2)

        self.p_data = [np.polynomial.polynomial.polyval(i,p.coef) for i in self.t_data]
        self.v_data = [np.polynomial.polynomial.polyval(i,v.coef) for i in self.t_data]
        self.a_data = [np.polynomial.polynomial.polyval(i,a.coef) for i in self.t_data]


    def __repr__(self) -> str:
        return self.info 
 

class Curve():

    def __init__(self, name, takt, zyklus):
        self.sections = []
        self.points = []

        self.name = name
        self.takt = takt
        self.zyklus = zyklus
        self.scale = 20

        self.set_data_zero()

    def set_data_zero(self):
        self.t = np.linspace(0,self.zyklus,num=self.zyklus*self.scale+1)
        self.p = np.zeros(self.zyklus*self.scale+1)
        self.v = np.zeros(self.zyklus*self.scale+1)
        self.a = np.zeros(self.zyklus*self.scale+1)

    def create_data_matrix (self): #to store curve data somewhere
        self.data_matrix = np.array([self.t,self.p,self.v,self.a])
    
    def delete_section(self): #to do
        pass

    def delete_curve(self): #to do
        pass

    def copy_curve(self): #to do
        pass

    def calculate_data(self):
        for sec in self.sections: #nur geraden und raste berechnen
            match sec.rule:
                case "Rast":
                    sec.calc_pause()
                case "v. const.":
                    sec.calc_vconst()
                case "Poly 5":
                    continue
                case "poly 5 connector":
                    continue
            if sec.t_s > sec.t_e:
                i_start = int(sec.t_s*self.scale)
                i_end = int(sec.t_e*self.scale+1)
                i_full = int(self.zyklus*self.scale+1)
                i_over = int(i_full+i_end)
                self.p[i_start:] = sec.p_data[i_start:i_full]
                self.p[:i_end] = sec.p_data[i_full:i_over]
                self.v[i_start:] = sec.v_data[i_start:i_full]
                self.v[:i_end] = sec.v_data[i_full:i_over]
                self.a[i_start:] = sec.a_data[i_start:i_full]
                self.a[:i_end] = sec.a_data[i_full:i_over]

            else:
                i_start = int(sec.t_s*self.scale)
                i_end = int(sec.t_e*self.scale+1)
                self.p[i_start:i_end] = sec.p_data[i_start:i_end]
                self.v[i_start:i_end] = sec.v_data[i_start:i_end]
                self.a[i_start:i_end] = sec.a_data[i_start:i_end]

        for sec in self.sections: #nur polynome berechnen
            match sec.rule:
                case "Rast":
                    continue
                case "v. const.":
                    continue
                case "Poly 5":
                    v0 = self.v[int(sec.t_s*self.scale)-1] #eventuel wieder einführen
                    a0 = self.a[int(sec.t_s*self.scale)-1]
                    v1 = self.v[int(sec.t_e*self.scale)]
                    a1 = self.a[int(sec.t_e*self.scale)]
                    # -===================== anfangsbedingungen die sehr klein sind auf 0 setzen --- sollte ev. besser gelöst werden indizes überprüfen (weshalb sind die AB manchmal nicht 0)
                    start_conditions = [self.v[int(sec.t_s*self.scale)-1],self.a[int(sec.t_s*self.scale)-1],self.v[int(sec.t_e*self.scale)],self.a[int(sec.t_e*self.scale)]]
                    for i, val in enumerate(start_conditions):
                        if val < 0.01 and val > -0.01:
                            start_conditions[i]=0

                    sec.calc_poly(v_s =start_conditions[0] , a_s =start_conditions[1] , v_e =start_conditions[2] , a_e =start_conditions[3])

                case "poly 5 connector":
                    v0 = self.v[int(sec.t_s*self.scale)] # hier auch
                    a0 = self.a[int(sec.t_s*self.scale)]
                    v1 = self.v[int(sec.t_e*self.scale)-1]
                    a1 = self.a[int(sec.t_e*self.scale)-1]
                    start_conditions = [self.v[int(sec.t_s*self.scale)],self.a[int(sec.t_s*self.scale)],self.v[int(sec.t_e*self.scale)-1],self.a[int(sec.t_e*self.scale)-1]]
                    for i, val in enumerate(start_conditions):
                        if val < 0.01 and val > -0.01:
                            start_conditions[i]=0

                    sec.calc_poly(v_s =start_conditions[0] , a_s =start_conditions[1] , v_e =start_conditions[2] , a_e =start_conditions[3])
            if sec.t_s > sec.t_e:
                i_start = int(sec.t_s*self.scale)
                i_end = int(sec.t_e*self.scale)
                i_full = int(self.zyklus*self.scale+1)
                i_over = int(i_full+i_end)
                self.p[i_start:] = sec.p_data[i_start:i_full]
                self.p[:i_end] = sec.p_data[i_full:i_over]
                self.v[i_start:] = sec.v_data[i_start:i_full]
                self.v[:i_end] = sec.v_data[i_full:i_over]
                self.a[i_start:] = sec.a_data[i_start:i_full]
                self.a[:i_end] = sec.a_data[i_full:i_over]

            else:
                i_start = int(sec.t_s*self.scale)
                i_end = int(sec.t_e*self.scale)
                self.p[i_start:i_end] = sec.p_data[i_start:i_end]
                self.v[i_start:i_end] = sec.v_data[i_start:i_end]
                self.a[i_start:i_end] = sec.a_data[i_start:i_end]

        self.data = np.array([self.t,self.p]) #v und a noch hinzufügen
    
    def delete_connection(self):
        for sec in self.sections:
            if sec.rule == "poly 5 connector":
                self.sections.remove(sec)

    def add_section(self,this_section):
        self.delete_connection()

        self.sections.append(this_section)

        if len(self.points) == 0:
            self.points.append([this_section.t_s, this_section.p_s])
            self.points.append([this_section.t_e, this_section.p_e])
        else:
            self.points.append([this_section.t_e, this_section.p_e])

        if self.get_total_time() != self.zyklus:
            self.create_connection(this_section.pos)
        
        self.calculate_data()
    
    def update_section(self, this_section,new_t_end,new_p_end,new_rule):
        self.points[this_section.pos][0] = new_t_end
        self.points[this_section.pos][1] = new_p_end
        this_section.rule = new_rule
        this_section.t_e = new_t_end
        this_section.p_e = new_p_end
        
        #change folowing section //////// what if its last section?
        self.sections[this_section.pos].t_s = new_t_end
        self.sections[this_section.pos].p_s = new_p_end


        self.set_data_zero()
        this_section.update_section_info()
        if self.get_total_time() != self.zyklus:
            self.create_connection(this_section.pos)
        self.calculate_data()
    
    def create_section(self,t_start, t_end, p_start, p_end, position_in_curve ,rule) -> Section:
        new_section = Section(t_start , t_end, p_start, p_end, position_in_curve, rule, self.zyklus, self.scale)
        return new_section

    def delete_connection(self,):

        for sec in self.sections:
            if sec.rule == "poly 5 connector":
                self.sections.remove(sec)

    def create_connection(self,pos):

        this_pos = pos + 1

        this_t_s = self.sections[-1].t_e
        if self.sections[0].t_s == 0:
            this_t_e = 360
        else:
            this_t_e = self.sections[0].t_s
        this_p_s = self.sections[-1].p_e
        this_p_e = self.sections[0].p_s

        connect_section = self.create_section(this_t_s , this_t_e, this_p_s, this_p_e, this_pos, "poly 5 connector")
        self.sections.append(connect_section)

    def get_number_of_sections(self) -> int:
        if len(self.sections) == 0:
            return 0
        else:
            result = len(self.sections) - 1
            return result

    def get_total_time(self):
        time = 0
        for sec in self.sections:
            if sec.t_s > sec.t_e:
                time = time + sec.t_e + self.zyklus - sec.t_s
            else:
                time = time + sec.t_e - sec.t_s
        return time
            

    def handle_over_360(self):
        #if ts > te -> drüber rechnen und ansetzen
        pass

    def __repr__(self) -> str: #to do
        pass

    def __str__(self) -> str: #to do
        pass



