from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg

from .config import api_key
from .request import PlayerNameNotFound, HypixelAPICallError, player_data
from .api_handle import HypixelInformationHandle as HIH

Hypixel = on_command('hypixel', permission=GROUP, aliases={'hyp'}, priority=0, block=True)
@Hypixel.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    '''/hypixel (ID) [bw]'''
    args = str(arg).split()
    reply = MessageSegment.reply(event.message_id)
    if api_key not in [None, 'API_KEY']:
        if len(args) >= 1:
            try:
                Original_data = await player_data(args[0], api_key)
                data = HIH(Original_data)
                if len(args) == 1:
                    msg = f'{data.Rank} {args[0]} 的Hypixel大厅信息：\n在线情况: {data.online} | Hypixel大厅等级: {data.level}\n最后登录时间: {data.last_login}\n起床战争数据查询：/hyp {args[0]} bw'
                if len(args) == 2:
                    if args[1] in ['bw','bedwars','起床']:
                        if data.bw_data_status == 'success':
                            msg = '\n'.join(
                                [
                                    f"[{data.bw_level}] {data.Rank} {args[0]} 的起床战争数据:",
                                    f"经验: {data.bw_experience} | 硬币: {format(data.bw_coin, ',d')} | 连胜: {format(data.winstreak, ',d')}",
                                    f"拆床: {format(data.break_bed, ',d')} | 被拆床: {format(data.lost_bed, ',d')} | BBLR: {data.BBLR}",
                                    f"胜场: {format(data.bw_win, ',d')} | 败场: {format(data.bw_losses, ',d')} | W/L: {data.W_L}",
                                    f"击杀: {format(data.bw_kill, ',d')} | 死亡: {format(data.bw_death, ',d')} | K/D: {data.K_D}",
                                    f"终杀: {format(data.bw_final_kill, ',d')} | 终死: {format(data.bw_final_death, ',d')} | FKDR: {data.FKDR}",
                                    f"收集铁锭: {format(data.bw_iron, ',d')} | 收集金锭: {format(data.bw_gold, ',d')}",
                                    f"收集钻石: {format(data.bw_diamond, ',d')} | 收集绿宝石: {format(data.bw_emerald, ',d')}"
                                ]
                            )
                        else: 
                            await Hypixel.finish(reply + '此玩家的起床战争数据不存在')
                await Hypixel.finish(reply + msg)
            except (PlayerNameNotFound, HypixelAPICallError) as e:
                await Hypixel.finish(reply + str(e))
        else:
            await Hypixel.finish(reply + '缺少必要参数！')
    else:
        await Hypixel.finish(reply + '请填写API密钥\n获取方式：\n在Hypixel服务器中输入指令:/api')