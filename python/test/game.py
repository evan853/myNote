#coding:utf-8
#################
# ϰ��45:��������һ����Ϸ
#################
# ǰ��
# 

#����Ҫ����һ����Ϸ����������μǣ���ɮ�ȳ�����յĹ��£�
#��ɮ��������ָɽ�£���������ձ�ѹ�š�����Ҫ�ȳ�����գ�
#��˵�������Լ�ȥ����ȡ�������Ǿȳ�������������أ�
#1.������ָɽ��ɽ��
#2.��ɽ����bos���ֱ����˯��
#3.˺��ɽ���ķ�ӡ��һ�����ܵ�ɽ�ס������ܱ�bos�Ե�
#4.������մ��Ͻ�����
#5.gameover


class Scene(object):
    status = ''    #��ǵ�ǰλ��
    
    def input(self):    #����
        say = raw_input('more-> ')   
        #print say
        return say
        
    def enter(self):   # enter()������ʾ��ǰ��λ��
        print '-'*5
        print "�����ڵ�λ���ǣ�", self.status
        print '-'*5
        
class DownHill(Scene):
    status = 'ɽ��'
#    def __init__(self):  #�ڳ�ʼ����д���λ�û�������Ρ������� �ʼǣ���2
#        self.enter()    #�̳и����enter()����  
          
    def talk(self): 
        super(DownHill, self).enter()             
        print 'ɽ������һ���˱�ɽѹס�ˡ�'
        print '���ȥ������̸��'
        print '��˵��ʩ�����Ǻ���Ϊ�α�ѹ����ָɽ�£�'
        self.input()
        print """�����˵����������գ�����ΪΥ����������������ѹ������ָɽ��,\n��������꣬��ɮ����Ⱦ���!"""
        self.input()
        print '��˵����Ӧ����ô���أ�'
        self.input()
        print '�����˵����Ҫ����ָɽ��ɽ�������ɽ����bos��˺������','�ҾͿ���\n�����ˡ���������֮���ұر����ɮ��'
        self.input()
        print '����һ��ʤ���߼������������ӷ�ʩ���ȴ�Ƭ�̱��ǡ�'
        print '#������ȥ���㱼����ָɽ���ˡ�'
        return 'hill'

class Hill(Scene):
    status = 'ɽ��'
   
    def talk(self):
        super(Hill, self).enter()
        for x in range(0, 10):
            print "��ɽ�У���������ͷ��"
            self.input()
        print '#ͻȻ�콵һ������:'
        print '�����أ��ҿ�����ľ��ˣ��ʷ�����ȥ�������������������·����'
        return 'top'

class TopHill(Scene):
    status = 'ɽ��'
    def bit(self):    #��ζȻ�BOS
       
        while self.input() != '':
            print '���ڶȻ�bos'
            
        print "��ɹ��ضȻ���BOS��"
     
               
    def talk(self):
        super(TopHill, self).enter() #super�����enter()����         
        print "#ͻȻ�ĳ�һ��ֻ�����׶��BOS"
        self.input()
        print "bos:��Ҫ�����㣡"
        self.input()
        print '#��ʱ������������ˡ�'
        self.bit()   #�������е�bit()����
        print '#BOS,���������˷�ӡ����'
        self.input()
        print '��˺������ӡ'
        self.input()
        print 'Bos,ͻȻ��������������'
        print '������ѡ��1.���¶Ȼ���\n\t2.��ͷ����'
        if self.input() == '1':
            print '�㱻�Ե��ˣ�Game Over��'
            exit(1)
        else:
            print '���ڷ�����ɽ���ܡ�'
            return 'return'
            
class ReturnDownHill(DownHill):
    
    def talk(self):
        super(ReturnDownHill, self).enter()
        print '�������������������������bos����׷������'
        print '���ʱ������ճ����ˣ�һ���Ӵ������׶��BOS'
        print '.0......�����ܶ�Ի�'
        print '����մ����˽𹿣�������ɮ����ȡ��ȥ��'
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