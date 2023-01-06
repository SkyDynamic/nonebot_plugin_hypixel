import time
from .request import HypixelAPICallError

class HypixelInformationHandle():
    def __init__(self, data: dict):
        #初始化数据
        online = data.get('online')
        data = data.get('player')
        '---基本数据---'
        #是否在线
        if online == True:
            self.online = '在线'
        else:
            self.online = '离线'
        #最后登陆的时间
        if data.get('lastLogin'):
            time_array = time.localtime(int(data.get('lastLogin')/1000))
            self.last_login = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        else:
            self.last_login = '对方隐藏了最后的上线时间'
        #Rank获取
        rank_id = data.get('newPackageRank')
        if rank_id == None:
            self.Rank = ''
        elif rank_id:
            if rank_id == 'VIP' or rank_id == 'MVP':
                self.Rank = f'[{rank_id}]'
            elif rank_id == 'VIP_PLUS' or rank_id == 'MVP_PLUS':
                self.Rank = f'[{str(rank_id).replace("_PLUS", "+")}]'
        #等级
        xp = data.get('networkExp')
        self.level = self.Get_Hypixel_Level(int(xp))
        '---小游戏元数据---'
        stats_data = dict(data.get('stats'))
        if stats_data:
            '---起床战争数据---'
            bedwars_data = stats_data.get('Bedwars')
            self.bw_data_status = 'failed'
            if bedwars_data:
                self.bw_data_status = 'success'
                #基本信息
                self.Get_Hypixel_Bedwars_Level(int(bedwars_data.get('Experience')))#等级
                self.bw_coin = bedwars_data.get('coins')#硬币
                self.winstreak = bedwars_data.get('winstreak')#连胜
                #床
                self.break_bed = bedwars_data.get('beds_broken_bedwars')#破坏床数
                self.lost_bed = bedwars_data.get('beds_lost_bedwars')#被破坏床数
                self.BBLR = round(self.break_bed / self.lost_bed, 3)#破坏床数和被破坏床数的比
                #胜败
                self.bw_win = bedwars_data.get('wins_bedwars')#胜利
                self.bw_losses = bedwars_data.get('losses_bedwars')#失败
                self.W_L = round(self.bw_win / self.bw_losses, 3)#胜利和失败的比
                #普通击杀/死亡
                self.bw_kill = bedwars_data.get('kills_bedwars')#击杀
                self.bw_death = bedwars_data.get('deaths_bedwars')#死亡
                self.K_D = round(self.bw_kill / self.bw_death, 3)#KD值
                #最终击杀/死亡
                self.bw_final_kill = bedwars_data.get('final_kills_bedwars')#最终击杀
                self.bw_final_death = bedwars_data.get('final_deaths_bedwars')#最终死亡
                self.FKDR = round(self.bw_final_kill / self.bw_final_death, 3)#最终KD值
                #矿物收集
                self.bw_iron = bedwars_data.get('iron_resources_collected_bedwars') if bedwars_data.get('iron_resources_collected_bedwars') else 0 #铁锭收集
                self.bw_gold = bedwars_data.get('gold_resources_collected_bedwars') if bedwars_data.get('gold_resources_collected_bedwars') else 0 #金锭收集
                self.bw_diamond = bedwars_data.get('diamond_resources_collected_bedwars') if bedwars_data.get('diamond_resources_collected_bedwars') else 0 #钻石收集
                self.bw_emerald = bedwars_data.get('emerald_resources_collected_bedwars') if bedwars_data.get('emerald_resources_collected_bedwars') else 0 #绿宝石收集
        else:
            raise HypixelAPICallError('玩家数据不存在')

    def Get_Hypixel_Level(self, xp: int) -> int:
        '''大厅等级算法'''
        prefix = -3.5
        const = 12.25
        divides = 0.0008
        return int((divides*xp+const)**0.5+prefix+1)

    def Get_Hypixel_Bedwars_Level(self, Exp: int) -> int:
        '''起床等级算法'''
        if Exp < 500:
            level = '0✫'
            experience = str(Exp) + '/500'
        elif Exp >= 500 and Exp < 1500:
            level = '1✫'
            experience = str(Exp-500) + '/1k'
        elif Exp >= 1500 and Exp < 3500:
            level = '2✫'
            experience = str(Exp-1500) + '/2k'
        elif Exp >= 3500 and Exp < 7000:
            level = '3✫'
            experience = str(Exp-3500) + '/3.5k'
        elif Exp >= 7000:
            if Exp < 487000:
                add_level = int((Exp-7000) / 5000)
                level = str(4+add_level) + '✫'
                experience = str(Exp-7000-add_level*5000) + '/5k'
            if Exp >= 487000:
                surplus_experience = Exp - (int(Exp / 487000)) * 487000
                if surplus_experience < 500:
                    add_level = 0
                    experience = str(surplus_experience) + '/500'
                elif surplus_experience >= 500 and surplus_experience < 1500:
                    add_level = 1
                    experience = str(surplus_experience-500) + '/1k'
                elif surplus_experience >= 1500 and surplus_experience < 3500:
                    add_level = 2
                    experience = str(surplus_experience-1500) + '/2k'
                elif surplus_experience >= 3500 and surplus_experience < 7000:
                    add_level = 3
                    experience = str(surplus_experience-3500) + '3.5k'
                elif surplus_experience >= 7000:
                    add_level = int((surplus_experience-7000) / 5000)
                    experience = str(surplus_experience-7000-add_level*5000)
                level = str((int(Exp/487000))*100+ 4 + add_level) + '✫'
        self.bw_level = level
        self.bw_experience = experience