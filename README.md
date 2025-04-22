# 腹黑法师的集会

桌游腹黑法师的集会随机角色选择器，确定游戏玩家人数已经玩家名称后可以随机发牌供玩家选择。

自定义法师和技能可以在在[法师数据库](src/wizards.py)中修改。现有规则参见[现有法师列表](doc/现有法师列表.txt)。

## 用法

直接运行：

```
python main.py --n_player 6 --player_names Player_1 Player_2 Player_3 Player_4 Player_5 Player_6 --n_select 3 --exclude_list 炼金术士 仙女
```

使用[MakeFile](makefile):

按照需要更新[makefile](makefile)中的玩家人数，名称，可选择法师数，以及排除法师列表之后，在此路径下运行```make```。

运行以下指令来避免同步makefile:
```
git update-index --assume-unchanged makefile
```

## 规则补充
- 职业 > 牌面 > 技能
- 被法反的的法术也可以抽牌
- [原版规则](doc/腹黑法师集会整合版说明书.pdf)

## 版权说明
本项目是一个非官方的、粉丝自制的工具，仅用于学习与交流目的。
- [法师数据库](src/wizards.py)中包含原版游戏中的39个法师及其描述，数据来自[原版规则](doc/腹黑法师集会整合版说明书.pdf)。
- 请支持正版，购买官方桌游以获取完整的角色和游戏体验。
- 所有原始桌游中的角色与内容版权均归 [文狗工作室] 所有。

如果您是版权持有者并希望我们下架相关内容，请随时联系。