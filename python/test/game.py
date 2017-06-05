#coding:utf-8
#################
# 习题45:你来制作一个游戏
#################
# 前言
# 

#我想要制作一个游戏，题材是西游记，唐僧救出孙悟空的故事：
#唐僧来到了五指山下，发现孙悟空被压着。他想要救出孙悟空，
#并说服他和自己去西天取经。但是救出孙悟空困难重重：
#1.爬到五指山的山顶
#2.给山顶的bos念经，直到它睡着
#3.撕掉山顶的封印，一口气跑到山底——不能背bos吃掉
#4.给孙悟空带上紧箍咒
#5.gameover


class Scene(object):
    status = ''    #标记当前位置
    
    def input(self):    #输入
        say = raw_input('more-> ')   
        #print say
        return say
        
    def enter(self):   # enter()用于显示当前的位置
        print '-'*5
        print "你现在的位置是：", self.status
        print '-'*5
        
class DownHill(Scene):
    status = '山脚'
#    def __init__(self):  #在初始化里写输出位置会输出两次——参照 笔记：类2
#        self.enter()    #继承父类的enter()方法  
          
    def talk(self): 
        super(DownHill, self).enter()             
        print '山脚下有一个人被山压住了。'
        print '你过去和他交谈：'
        print '你说：施主你是何人为何被压在五指山下？'
        self.input()
        print """孙悟空说：我是孙悟空，我因为违反天条被如来佛祖压在这五指山下,\n整整五百年，高僧请你救救我!"""
        self.input()
        print '你说：我应该怎么办呢？'
        self.input()
        print '孙悟空说：你要到五指山的山顶，打败山顶的bos。撕掉符文','我就可以\n脱身了。带我脱身之后我必报答高僧。'
        self.input()
        print '救人一命胜造七级浮屠，阿弥陀佛！施主等待片刻便是。'
        print '#你起身去，便奔向五指山顶了。'
        return 'hill'

class Hill(Scene):
    status = '山上'
   
    def talk(self):
        super(Hill, self).enter()
        for x in range(0, 10):
            print "爬山中，看不到尽头！"
            self.input()
        print '#突然天降一道神域:'
        print '唐三藏，我看你诚心救人，故放你上去，但生死有命。下面的路。。'
        return 'top'

class TopHill(Scene):
    status = '山顶'
    def bit(self):    #如何度化BOS
       
        while self.input() != '':
            print '你在度化bos'
            
        print "你成功地度化了BOS。"
     
               
    def talk(self):
        super(TopHill, self).enter() #super父类的enter()方法         
        print "#突然蹦出一个只长相凶恶的BOS"
        self.input()
        print "bos:我要吃了你！"
        self.input()
        print '#是时候给他讲道理了。'
        self.bit()   #调用类中的bit()方法
        print '#BOS,带你来到了封印处。'
        self.input()
        print '你撕下来封印'
        self.input()
        print 'Bos,突然发狂，向你扑来。'
        print '请做出选择：1.重新度化它\n\t2.掉头就跑'
        if self.input() == '1':
            print '你被吃掉了，Game Over！'
            exit(1)
        else:
            print '你在疯狂的往山下跑。'
            return 'return'
            
class ReturnDownHill(DownHill):
    
    def talk(self):
        super(ReturnDownHill, self).enter()
        print '你气喘嘘嘘的跑了下来，但是bos还紧追你的身后。'
        print '这个时候孙悟空出现了，一棒子打死了凶恶的BOS'
        print '.0......经过很多对话'
        print '孙悟空带上了金箍，保护唐僧西天取经去了'
        exit(1)
        
       
class Map(object):

    scenes = {
              'down': DownHill(),
              'hill': Hill(),
              'top': TopHill(),
              'return': ReturnDownHill()
              }
    def __init__(self, start_scene):
        self.start_scene = start_scene 
        
    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)
    
    def opening_scene(self):
        return self.next_scene(self.start_scene)
        
class Engine(object):
    def __init__(self, scene_map):
        self.scene_map = scene_map
        
    def play(self):
        current_scene = self.scene_map.opening_scene()
        
        while True:
            next_scene_name = current_scene.talk()
            current_scene = self.scene_map.next_scene(next_scene_name)      
              
a_map = Map('down')
print type(a_map.opening_scene())
print Map.scenes
a_game = Engine(a_map)
#a_game.play()