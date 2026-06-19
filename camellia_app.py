# camellia_app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# =============== 数据部分（内嵌，无需外部文件）===============
periods = {
    "晚中新世（8 Ma）": {
        "time_range": "约800万年前",
        "climate": {"mat": 17.5, "map": 1400},
        "elevation": "1500–2900 m",
        "vegetation": "亚热带常绿阔叶林",
        "companions": ["栲属", "石栎", "木荷", "樟科"],
        "camellia_traits": {
            "height": "3–6 m",
            "flower_size": "5–7 cm",
            "flower_color": "粉红至淡红",
            "leaf_shape": "椭圆形，革质",
            "growth_form": "林下小乔木"
        },
        "distribution": [(25.0, 100.0), (24.5, 101.0)],
        "culture": None,
        "evidence": "小龙潭化石孢粉组合、分子钟推演",
        "image": None
    },
    "上新世（3 Ma）": {
        "time_range": "约300万年前",
        "climate": {"mat": 16.0, "map": 1250},
        "elevation": "1600–2800 m",
        "vegetation": "常绿-落叶混交林",
        "companions": ["青冈", "桦木", "杜鹃"],
        "camellia_traits": {
            "height": "4–7 m",
            "flower_size": "6–9 cm",
            "flower_color": "深红",
            "leaf_shape": "长椭圆，微锯齿",
            "growth_form": "林缘灌木至小乔木"
        },
        "distribution": [(25.2, 100.2), (24.8, 100.8)],
        "culture": None,
        "evidence": "滇西湖泊沉积记录",
        "image": None
    },
    "全新世中期（6 ka）": {
        "time_range": "距今6000年",
        "climate": {"mat": 16.5, "map": 1300},
        "elevation": "1700–2700 m",
        "vegetation": "湿润常绿阔叶林",
        "companions": ["栲", "多依", "含笑", "竹类"],
        "camellia_traits": {
            "height": "5–8 m",
            "flower_size": "8–10 cm",
            "flower_color": "艳红",
            "leaf_shape": "卵状椭圆形",
            "growth_form": "林窗优势种"
        },
        "distribution": [(25.1, 100.1), (25.5, 100.5)],
        "culture": "可能被早期人类采集利用",
        "evidence": "洱海、滇池花粉谱",
        "image": None
    },
    "南诏-大理国时期（9–13世纪）": {
        "time_range": "公元9–13世纪",
        "climate": {"mat": 15.8, "map": 1200},
        "elevation": "1800–2600 m",
        "vegetation": "寺庙次生林 + 天然常绿阔叶林",
        "companions": ["栲", "多依", "松", "柏"],
        "camellia_traits": {
            "height": "5–8 m",
            "flower_size": "8–12 cm",
            "flower_color": "深红，初现重瓣",
            "leaf_shape": "阔椭圆，革质光亮",
            "growth_form": "庭院与林缘兼有"
        },
        "distribution": [(25.38, 100.55), (25.22, 100.30)],  # 水目山、巍宝山
        "culture": "佛教‘曼陀罗花’，899年《南诏中兴画卷》绘录，水目山唐代茶花王始植",
        "evidence": "《南诏中兴画卷》、古树碳14测年",
        "image": "images/shuimu_tang.jpg"
    },
    "明代（14–17世纪）": {
        "time_range": "公元14–17世纪",
        "climate": {"mat": 14.8, "map": 1050},
        "elevation": "1800–2600 m",
        "vegetation": "次生林 + 人工庭院",
        "companions": ["松", "柏", "玉兰", "桂花"],
        "camellia_traits": {
            "height": "2–5 m（修剪后）",
            "flower_size": "10–15 cm（选育品种）",
            "flower_color": "大红、粉红、复色",
            "leaf_shape": "宽椭圆，光亮",
            "growth_form": "庭院观赏灌木"
        },
        "distribution": [(25.04, 102.72), (25.85, 100.50)],  # 昆明金殿、鸡足山
        "culture": "徐霞客见丽江木府‘楼前茶树’；《滇南茶花小志》载28品；杨升庵诗赞",
        "evidence": "地方志、古树年龄测定",
        "image": "images/jindian_ming.jpg"
    },
    "清代至民国（18–20世纪）": {
        "time_range": "公元18–20世纪中",
        "climate": {"mat": 15.2, "map": 1100},
        "elevation": "1800–2600 m",
        "vegetation": "残存天然林 + 寺院保护林",
        "companions": ["寺院绿化树", "竹", "梅"],
        "camellia_traits": {
            "height": "3–6 m",
            "flower_size": "9–14 cm",
            "flower_color": "紫红、深红（如‘紫袍’）",
            "leaf_shape": "椭圆至卵圆",
            "growth_form": "半野生状态"
        },
        "distribution": [(25.85, 100.50), (24.88, 100.00)],  # 鸡足山、凤庆
        "culture": "90%古树存于寺庙；大理‘朝花节’盛行",
        "evidence": "古树普查、口述史",
        "image": "images/jizu_zipao.jpg"
    },
    "现代（1950s–今）": {
        "time_range": "当代",
        "climate": {"mat": 15.5, "map": 1100},
        "elevation": "1800–2600 m（人工扩展至低海拔）",
        "vegetation": "城市绿地、专类园、残存天然林",
        "companions": ["园林绿化树种", "草坪"],
        "camellia_traits": {
            "height": "1–4 m（园艺控制）",
            "flower_size": "8–20 cm（重瓣品种）",
            "flower_color": "红、粉、白、复色、镶边",
            "leaf_shape": "多样，部分品种叶背有绒毛",
            "growth_form": "高度人工选育"
        },
        "distribution": [
            (25.04, 102.72),  # 昆明金殿
            (25.85, 100.50),  # 宾川鸡足山
            (25.22, 100.30)   # 巍山巍宝山
        ],
        "culture": "云南省花；昆明茶花节；国家Ⅱ级保护植物；全省古树超5万株",
        "evidence": "《云南山茶志》、IUCN评估、2024古树普查",
        "image": "images/modern_gushu.jpg"
    }
}

# =============== 辅助函数 ===============
def plot_ecological_profile(period_name):
    """绘制生态剖面图（支持中文）"""
    # === 关键修复：设置中文字体 ===
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # 基础分层
    layers = [
        {"name": "乔木层", "height": 25, "color": "#2e7d32", "label": "栲、石栎"},
        {"name": "亚乔木层", "height": 12, "color": "#4caf50", "label": "山茶、木荷"},
        {"name": "灌木层", "height": 4, "color": "#8bc34a", "label": "杜鹃、小檗"},
        {"name": "草本层", "height": 1, "color": "#cddc39", "label": "蕨类、苔藓"}
    ]
    
    # 人工时期特殊处理
    if any(kw in period_name for kw in ["南诏", "明代", "清代", "现代"]):
        layers = [
            {"name": "孤立古树", "height": 8, "color": "#e91e63", "label": "云南山茶"},
            {"name": "庭院地被", "height": 1, "color": "#795548", "label": "铺装/草坪"}
        ]
    
    y = 0
    for layer in layers:
        height = layer["height"]
        ax.barh([0], [height], left=y, color=layer["color"], edgecolor='k', alpha=0.8)
        ax.text(y + height/2, 0, f"{layer['name']}\n{layer['label']}", 
                ha='center', va='center', fontsize=8, color='white')
        y += height
    
    ax.set_xlim(0, max(30, y))
    ax.set_ylim(-0.5, 0.5)
    ax.axis('off')
    ax.set_title(f"生态剖面示意（{period_name}）", fontsize=10)
    return fig

# =============== Streamlit 主界面 ===============
st.set_page_config(
    page_title="云南山茶四维演化模型",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 云南山茶（*Camellia reticulata*）四维演化模型")
st.markdown("""
从 **800万年前** 到 **今日**，探索云南山茶的生态、形态与文化演变。
> 整合古植物学、气候重建、古树调查与历史文献
""")

# 选择时期
selected = st.selectbox("请选择历史时期", list(periods.keys()))
data = periods[selected]

# 分栏布局
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("🌍 气候与生境")
    st.write(f"**时期**：{data['time_range']}")
    st.write(f"**年均温**：{data['climate']['mat']} °C")
    st.write(f"**年降水**：{data['climate']['map']} mm")
    st.write(f"**海拔范围**：{data['elevation']}")
    st.write(f"**植被类型**：{data['vegetation']}")
    
    st.subheader("🌿 伴生植物")
    st.write("、".join(data['companions']))
    
    if data['culture']:
        st.subheader("🏯 人类文化")
        st.info(data['culture'])
    
    st.subheader("📚 科学证据")
    st.caption(data['evidence'])

with col2:
    st.subheader("📍 推演分布（示意）")
    m = folium.Map(
        location=[25.0, 100.0],
        zoom_start=7,
        tiles="CartoDB positron"
    )
    for lat, lon in data['distribution']:
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color="#c0392b",
            fill=True,
            fill_color="#e74c3c",
            fill_opacity=0.8,
            popup=f"{selected}<br>云南山茶适生区"
        ).add_to(m)
    st_folium(m, width=600, height=400)

# 形态特征卡片
st.subheader("🌸 形态特征演化")
traits = data['camellia_traits']
cols = st.columns(5)
cols[0].metric("株高", traits['height'])
cols[1].metric("花径", traits['flower_size'])
cols[2].write(f"**花色**\n{traits['flower_color']}")
cols[3].write(f"**叶形**\n{traits['leaf_shape']}")
cols[4].write(f"**生长型**\n{traits['growth_form']}")

# ================= 新增多媒体区 =================
st.markdown("---")
st.subheader("📸 典型古树与形态演化")

# 生态剖面图
st.subheader("🌳 生态结构剖面")
st.pyplot(plot_ecological_profile(selected))

# 底部说明
st.markdown("---")
st.caption("本模型为科研教育用途。真实古环境重建需结合花粉、古DNA、同位素等多源数据。")
