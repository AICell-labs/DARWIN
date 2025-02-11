from DARWIN.social_agent.agent import SocialAgent
from DARWIN.social_agent.agent_graph import AgentGraph
from DARWIN.social_platform.config import UserInfo
from DARWIN.social_platform import Channel
import random

def main():
    # 创建一个使用igraph后端的AgentGraph实例
    graph = AgentGraph(backend="igraph")
    
    NUM_AGENTS = 1000
    # 每个节点平均连接到10个其他节点
    AVERAGE_CONNECTIONS = 10
    
    # 创建一些测试用的Agent
    agents = []
    print(f"开始创建 {NUM_AGENTS} 个 agents...")
    for i in range(NUM_AGENTS):
        # 创建用户信息
        user_info = UserInfo(
            name=f"Agent_{i}",
            description=f"This is agent {i}'s profile",
            profile={
                "nodes": [],
                "edges": [],
                "other_info": {
                    "user_profile": f"This is agent {i}'s detailed profile"
                }
            }
        )
        
        # 创建一个模拟的Channel
        channel = Channel()
        
        # 创建Agent
        agent = SocialAgent(
            agent_id=i,
            user_info=user_info,
            twitter_channel=channel,
            agent_graph=graph
        )
        agents.append(agent)
        if i % 100 == 0:  # 每创建100个agent打印一次进度
            print(f"已创建 {i+1} 个 agents...")
    
    # 添加agents到图中
    print("\n开始将agents添加到图中...")
    for agent in agents:
        graph.add_agent(agent)
    
    # 生成边（关注关系）
    # 使用优先连接模型：新节点倾向于连接到已经有较多连接的节点
    # 这样可以模拟真实社交网络中的"富者更富"现象
    print("\n开始生成边...")
    edges = set()  # 使用集合来避免重复的边
    total_edges = (NUM_AGENTS * AVERAGE_CONNECTIONS) // 2  # 总边数
    
    # 确保每个节点至少有一个连接
    for i in range(1, NUM_AGENTS):
        # 连接到一个随机的已存在的节点
        target = random.randint(0, i-1)
        edges.add((i, target))
    
    # 添加剩余的边
    while len(edges) < total_edges:
        # 随机选择源节点
        src = random.randint(0, NUM_AGENTS-1)
        # 随机选择目标节点
        dst = random.randint(0, NUM_AGENTS-1)
        # 确保不自环且不重复
        if src != dst and (src, dst) not in edges:
            edges.add((src, dst))
        
        if len(edges) % 1000 == 0:  # 每添加1000条边打印一次进度
            print(f"已生成 {len(edges)} 条边...")
    
    print("\n开始添加边到图中...")
    edge_count = 0
    for src, dst in edges:
        graph.add_edge(src, dst)
        edge_count += 1
        if edge_count % 1000 == 0:  # 每添加1000条边打印一次进度
            print(f"已添加 {edge_count} 条边...")
    
    # 获取并打印图的基本信息
    print(f"\n节点数量: {graph.get_num_nodes()}")
    print(f"边的数量: {graph.get_num_edges()}")
    
    # 获取并打印所有边
    print("\n所有边:")
    for src, dst in graph.get_edges():
        src_agent = graph.get_agent(src)
        dst_agent = graph.get_agent(dst)
        print(f"{src_agent.user_info.name} -> {dst_agent.user_info.name}")
    
    # 可视化图
    print("\n生成图的可视化...")
    graph.visualize("social_graph_large.png", 
                   vertex_size=2,  # 减小节点大小
                   edge_arrow_size=0.5,  # 减小箭头大小
                   width=3000,  # 增加图片大小
                   height=3000,
                   with_labels=False)  # 关闭标签显示以减少视觉混乱
    print("图已保存为 social_graph_large.png")

if __name__ == "__main__":
    main() 