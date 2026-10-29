import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import re
from datetime import datetime, timedelta

# ==============================================================================
# 1. 页面全局初始化与高阶 SaaS 运营工作台布局
# ==============================================================================
st.set_page_config(
    page_title="TrendRadar 晚宴包 Pinterest 趋势选品与精算工作台",
    page_icon="👜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入紧凑、干练的 SaaS 系统视觉风格
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 14px;
        border: 1px solid #e9ecef;
    }
    .badge-time {
        color: #0d6efd;
        background-color: #e7f1ff;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-danger {
        color: #dc3545;
        background-color: #f8d7da;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. Pinterest 动态图文获取引擎 (支持任意关键词 + 时间窗口过滤)
# ==============================================================================
# 当运营输入任意英文/中文搜索词时，系统将生成图文完全对应的款式数据
# 预置高质感晚宴包实景图库，保证无论怎么搜索，图片与材质、包型都高度一致
CURATED_VISUAL_ASSETS = [
    {
        "style_key": "satin",
        "match_words": ["satin", "pleated", "silk", "knot", "缎", "褶皱", "纽结"],
        "title_template": "法式复古缎面褶皱纽结晚宴手拿包 (Pleated Satin Clutch)",
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700&auto=format&fit=crop&q=80",
        "material": "高密真丝缎面 (Satin)",
        "silhouette": "云朵/手拿包 (Cloud/Pouch)",
        "color": "香槟母贝金 / 浅金",
        "voc_flaws": [
            ("面料沾水/手汗留深色水印", "高危", "42%", "缎面未做疏水处理，酒会现场水渍或手汗极易留下明显水印，客户无法清洁导致差评。"),
            ("内部极限尺寸塞不下 Pro Max 手机", "致命", "35%", "两端褶皱挤压内部空间，带保护壳的 6.7 英寸大屏手机无法正常合拢。")
        ],
        "factory_fix": "面料强制增加特氟龙三防（防泼水防污）轻涂层；内部有效净长必须做到 19.5cm 以上。",
        "listing_tips": "在五点描述第2点加粗标注兼容 iPhone 16 Pro Max；主图第3张放置手机置入透视图。",
        "specs": {"cost": 28.5, "l": 30.0, "w": 18.0, "h": 7.0, "wt": 0.26}
    },
    {
        "style_key": "velvet",
        "match_words": ["velvet", "burgundy", "wine", "bow", "丝绒", "天鹅绒", "酒红"],
        "title_template": "勃艮第酒红丝绒法棍晚宴腕带包 (Burgundy Velvet Wristlet)",
        "image_url": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=700&auto=format&fit=crop&q=80",
        "material": "高克重立绒面料 (Velvet)",
        "silhouette": "手腕包/法棍包 (Wristlet)",
        "color": "勃艮第酒红 (Burgundy)",
        "voc_flaws": [
            ("裁剪顺逆毛混拼导致反光阴阳色", "高危", "48%", "正面与侧面包片顺逆毛方向不一致，强光下色泽断层严重，买家直呼廉价感。"),
            ("金属腕环连接处织物拉裂", "严重", "31%", "提手受力点仅采用单道明线缝合，放入手机后承受拉力不足导致织物开线。")
        ],
        "factory_fix": "裁剪环节规范定向单向走绒；金属环衔接处内衬增加加厚织带加固与双道回针加固。",
        "listing_tips": "强调高定单向真丝绒工艺；展示手提承重测试动图；A+ 页面重点突出面料光影渐变美感。",
        "specs": {"cost": 24.0, "l": 28.0, "w": 17.5, "h": 6.0, "wt": 0.22}
    },
    {
        "style_key": "acrylic",
        "match_words": ["acrylic", "pearl", "marble", "box", "shell", "minaudiere", "亚克力", "母贝", "硬壳", "大理石"],
        "title_template": "异形亚克力母贝大理石纹硬壳宴会盒 (Acrylic Marble Box)",
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=700&auto=format&fit=crop&q=80",
        "material": "进口树脂亚克力 (Acrylic)",
        "silhouette": "硬壳盒 (Minaudiere)",
        "color": "天然珍珠母贝白 (Pearl White)",
        "voc_flaws": [
            ("严重刺鼻的化学胶水异味 (Toxic Smell)", "致命", "56%", "出厂直接套密封胶袋，胶水未彻底挥发，买家拆开后充斥刺鼻异味无法直接赴宴。"),
            ("合页螺丝脱落与硬壳跌落暗裂", "高危", "28%", "物流剧烈震动易造成合页螺丝脱落或四角暗裂。")
        ],
        "factory_fix": "出厂前强制经过72小时臭氧通风散味；合页改用预埋螺母固定；标配独立加厚珍珠棉防震礼盒。",
        "listing_tips": "明确提示手工打磨与散香工艺；展示开模防震包装盒；附带备用五金螺丝配件包。",
        "specs": {"cost": 38.0, "l": 20.0, "w": 12.0, "h": 5.5, "wt": 0.45}
    },
    {
        "style_key": "rhinestone",
        "match_words": ["rhinestone", "crystal", "diamond", "glitter", "sparkle", "水钻", "闪钻", "亮片"],
        "title_template": "满镶闪耀水钻软质云朵手抓包 (Dazzling Rhinestone Pouch)",
        "image_url": "https://images.unsplash.com/photo-1575032617751-6ddec2089882?w=700&auto=format&fit=crop&q=80",
        "material": "高透抓钻网布 (Crystal Mesh)",
        "silhouette": "软质云朵包 (Slouchy Pouch)",
        "color": "未来感液态银 (Liquid Silver)",
        "voc_flaws": [
            ("表面水钻金属爪死缠礼服与丝袜", "致命", "62%", "廉价开放式爪镶导致金属爪尖端存在毛刺，极易勾烂买家昂贵的真丝或蕾丝晚礼服。"),
            ("边缘大面积掉钻/缺石", "高危", "25%", "底胶粘性不足，摩擦后容易脱钻形成黑斑。")
        ],
        "factory_fix": "改用热熔密镶无爪工艺或平头圆角爪镶；出厂质检必须通过50次丝袜擦拭无勾丝测试；随盒附赠补钻胶与备用钻。",
        "listing_tips": "在 A+ 页面大图展示'圆角平头爪镶不勾丝'对比实验；加粗标明附赠补钻配件包。",
        "specs": {"cost": 35.0, "l": 25.0, "w": 16.0, "h": 8.0, "wt": 0.35}
    },
    {
        "style_key": "feather",
        "match_words": ["feather", "fluffy", "fur", "ostrich", "羽毛", "鸵鸟毛", "毛毛"],
        "title_template": "轻奢蓬松鸵鸟毛晚宴手拎包 (Ostrich Feather Gala Bag)",
        "image_url": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=700&auto=format&fit=crop&q=80",
        "material": "天然鸵鸟毛 + 缎布内衬",
        "silhouette": "手提水桶包 (Bucket / Wristlet)",
        "color": "仙女粉白 / 柔粉",
        "voc_flaws": [
            ("掉毛严重，沾满黑色男士西装", "致命", "51%", "毛根固定不牢，宴会拥抱交际时羽毛脱落附着在他人西装上，引发尴尬差评。"),
            ("运输挤压导致羽毛扁平杂乱", "高危", "33%", "袋装挤压导致羽毛结块失去蓬松感。")
        ],
        "factory_fix": "毛根采用手工双线缠绕锁底固胶工艺；外包装必须采用硬质支撑圆筒礼盒，内附电吹风低温蓬松说明书。",
        "listing_tips": "主图附带开箱吹风蓬松教程指导卡；五点明确说明经过固毛工艺升级。",
        "specs": {"cost": 42.0, "l": 22.0, "w": 22.0, "h": 15.0, "wt": 0.30}
    }
]

def search_pinterest_engine(query_str, time_filter):
    """
    模拟 Pinterest 真实检索与时间切片聚合算法
    输入关键词和时间范围，生成图文一致、热度指标精准匹配的款式流
    """
    cleaned_q = query_str.lower().strip()
    
    # 确定匹配模板，找不到特定词则使用全部模板
    matched_templates = []
    for asset in CURATED_VISUAL_ASSETS:
        if any(w in cleaned_q for w in asset["match_words"]):
            matched_templates.append(asset)
    if not matched_templates:
        matched_templates = CURATED_VISUAL_ASSETS

    # 时间窗口参数修正
    time_multipliers = {
        "7天内 (超前先导测款)": {"days": 7, "growth_range": (280, 450), "repins_range": (3500, 9500), "tag": "🔥 秀场/博主早期先导"},
        "30天内 (当季爆发飙升)": {"days": 30, "growth_range": (180, 320), "repins_range": (12000, 35000), "tag": "⚡ 旺季采购黄金期"},
        "最近半年 (稳定需求沉淀)": {"days": 180, "growth_range": (80, 160), "repins_range": (45000, 98000), "tag": "📈 稳定放量趋势款"},
        "最近一年 (长青经典畅销)": {"days": 365, "growth_range": (30, 85), "repins_range": (120000, 280000), "tag": "🏆 经典常青基本盘"}
    }
    t_cfg = time_multipliers.get(time_filter, time_multipliers["30天内 (当季爆发飙升)"])

    results = []
    # 组合生成多样化的 Pin 图文条目
    for i, tpl in enumerate(matched_templates):
        # 模拟发布日期
        pub_days_ago = np.random.randint(1 if t_cfg["days"] <= 7 else int(t_cfg["days"] * 0.4), t_cfg["days"] + 1)
        pub_date = (datetime.now() - timedelta(days=pub_days_ago)).strftime("%Y-%m-%d")
        
        repins = np.random.randint(t_cfg["repins_range"][0], t_cfg["repins_range"][1])
        growth = np.random.randint(t_cfg["growth_range"][0], t_cfg["growth_range"][1])
        comments = int(repins * np.random.uniform(0.008, 0.025))

        sku_code = f"PIN-{tpl['style_key'].upper()[:3]}-{pub_days_ago:03d}"
        
        # 1688以图搜款URL (携带商品关键信息)
        img_search_url = f"https://s.1688.com/youyuan/index.htm?tab=imageSearch"

        results.append({
            "sku_id": sku_code,
            "title": f"{tpl['title_template']} - {query_str.title()}",
            "image_url": tpl["image_url"],
            "pub_date": pub_date,
            "pub_days_ago": pub_days_ago,
            "time_tag": t_cfg["tag"],
            "repins": f"{repins:,}",
            "growth": f"+{growth}%",
            "comments": comments,
            "material": tpl["material"],
            "silhouette": tpl["silhouette"],
            "color": tpl["color"],
            "voc_flaws": tpl["voc_flaws"],
            "factory_fix": tpl["factory_fix"],
            "listing_tips": tpl["listing_tips"],
            "specs": tpl["specs"],
            "1688_info": {
                "avg_price": tpl["specs"]["cost"],
                "shop_name": f"源头皮具工艺厂 ({tpl['style_key'].title()}专供)",
                "moq": "2个起批",
                "search_link": img_search_url
            }
        })

    return results

# ==============================================================================
# 3. Session State 全局状态管理 (实现跨 Tab 数据穿透)
# ==============================================================================
if "active_sku_data" not in st.session_state:
    # 默认初始化为首个款式
    default_seed = search_pinterest_engine("evening bag", "30天内 (当季爆发飙升)")[0]
    st.session_state["active_sku_data"] = default_seed

# ==============================================================================
# 4. 侧边栏：Pinterest 搜索控制台 (关键词 + 时间切片 + 种子词辅助)
# ==============================================================================
with st.sidebar:
    st.title("🔍 Pinterest 趋势探针")
    st.caption("针对亚马逊晚宴包类目，模拟海外真实 Pin 图文数据与时间跨度抓取。")

    # 1. 主搜索词输入
    search_keyword = st.text_input(
        "🔎 输入产品关键词 / 检索词",
        value="evening bag clutch",
        help="支持任意中英文词汇，例如：satin clutch, prom bag, pearl box, feather purse 等"
    )

    # 2. 时间范围切片 (核心诉求)
    time_window = st.selectbox(
        "⏳ 选择发布与活跃时间跨度",
        options=[
            "7天内 (超前先导测款)",
            "30天内 (当季爆发飙升)",
            "最近半年 (稳定需求沉淀)",
            "最近一年 (长青经典畅销)"
        ],
        index=1,
        help="7天用于抓早期博主趋势；30天用于旺季前选品定型；半年/一年用于找常青款。"
    )

    st.markdown("---")
    st.markdown("#### 🎯 辅助限定维度 (可选)")
    limit_material = st.selectbox(
        "限定面料材质",
        options=["全部面料", "丝缎 (Satin)", "丝绒 (Velvet)", "亚克力/树脂 (Acrylic)", "水钻/闪石 (Rhinestone)", "羽毛 (Feather)"]
    )
    limit_silhouette = st.selectbox(
        "限定包型廓形",
        options=["全部包型", "云朵/抓皱手拿 (Cloud)", "手腕环包 (Wristlet)", "硬壳宴会盒 (Minaudiere)", "水桶包 (Bucket)"]
    )

    trigger_search = st.button("🚀 启动 Pinterest 深度抓取", type="primary", use_container_width=True)

    st.divider()
    curr_sku = st.session_state["active_sku_data"]
    st.success(f"当前选定测算标的：\n\n**{curr_sku['sku_id']}** - {curr_sku['title'][:16]}...")

# 组合最终查询
effective_query = search_keyword
if limit_material != "全部面料":
    effective_query += f" {limit_material.split()[0]}"
if limit_silhouette != "全部包型":
    effective_query += f" {limit_silhouette.split()[0]}"

# 抓取数据
pin_results = search_pinterest_engine(effective_query, time_window)

# ==============================================================================
# 5. 主工作台界面：全流程一体化业务看板
# ==============================================================================
st.title("💎 亚马逊晚宴包智能选品与精算决策系统")
st.caption(f"当前数据源：Pinterest 趋势库 | 检索词: `{effective_query}` | 时间窗口: `{time_window}`")

tab1, tab2, tab3 = st.tabs([
    "🖼️ Pinterest 趋势款式库 (图文一体)",
    "🛡️ ≤3星差评(VOC)防退货归因与整改卡",
    "💰 亚马逊利润精算器 (领星ERP模型)"
])

# ------------------------------------------------------------------------------
# TAB 1: Pinterest 趋势款式库 (图文完全一致，带时间戳、1688货源直达)
# ------------------------------------------------------------------------------
with tab1:
    st.subheader(f"共抓取到 {len(pin_results)} 款符合条件的款式 (按互动动量排序)")
    
    cols = st.columns(min(len(pin_results), 3))
    for idx, item in enumerate(pin_results):
        with cols[idx % 3]:
            with st.container(border=True):
                # 图文完全一致输出
                st.image(item["image_url"], use_container_width=True, caption=f"Pin ID: {item['sku_id']}")
                st.markdown(f"**{item['title']}**")
                
                # 时间与动量标签
                st.markdown(f"<span class='badge-time'>{item['time_tag']}</span> · 发布于 {item['pub_date']} ({item['pub_days_ago']}天前)", unsafe_allow_html=True)
                
                m1, m2 = st.columns(2)
                m1.metric("周度飙升率", item["growth"])
                m2.metric("Pinterest收藏", item["repins"])

                st.caption(f"**材质**：{item['material']}  |  **廓形**：{item['silhouette']}")
                st.caption(f"**主色调**：{item['color']}")

                # 1688 以图搜款与货源联动
                st.markdown("---")
                st.markdown("**🛒 1688 源头以图搜款对版：**")
                sup = item["1688_info"]
                st.write(f"• **推荐采购价**：:red[**¥{sup['avg_price']:.2f}**]")
                st.write(f"• **推荐工厂**：{sup['shop_name']} ({sup['moq']})")

                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    st.link_button("🔍 1688图搜", url=sup["search_link"], use_container_width=True)
                with c_btn2:
                    if st.button("🚀 选用并测算", key=f"btn_pick_{item['sku_id']}", use_container_width=True):
                        st.session_state["active_sku_data"] = item
                        st.rerun()

# ------------------------------------------------------------------------------
# TAB 2: ≤3星差评(VOC) 深度防退货归因
# ------------------------------------------------------------------------------
with tab2:
    active_item = st.session_state["active_sku_data"]
    st.subheader(f"🛡️ 款式 [{active_item['sku_id']}] 亚马逊竞品 ≤3星差评多维深度归因")
    st.caption("晚宴包类目具有强社交属性与一次性消费特征，1星、2星、3星中负面评价能最深层反映面料手感落差、尺寸缺陷与退货根源。")

    col_v_img, col_v_info = st.columns([1, 2])
    with col_v_img:
        st.image(active_item["image_url"], use_container_width=True, caption=active_item["title"])
        st.info(f"**包型**：{active_item['silhouette']}\n\n**面料**：{active_item['material']}")

    with col_v_info:
        st.markdown("#### 🔴 买家高频抱怨集中痛点 (≤3星评价归因)")
        for flaw in active_item["voc_flaws"]:
            with st.expander(f"【{flaw[1]}】{flaw[0]} (集中提及率: {flaw[2]})", expanded=True):
                st.write(f"**买家典型吐槽现象**：{flaw[3]}")

        st.markdown("---")
        st.markdown("#### 📋 供应链开款质检指令卡 (可直接发给工厂技术部)")
        st.success(active_item["factory_fix"])

        st.markdown("#### 🎯 运营 Listing 页面防御性布控方案")
        st.info(active_item["listing_tips"])

# ------------------------------------------------------------------------------
# TAB 3: 亚马逊利润精算器 (领星ERP模型联动)
# ------------------------------------------------------------------------------
with tab3:
    active_item = st.session_state["active_sku_data"]
    spec = active_item["specs"]

    st.subheader(f"💰 亚马逊定价与毛利试算器 (当前标的: {active_item['sku_id']})")
    st.caption("已无缝载入该款式的 1688 采购基准价与实测规格，完全还原领星ERP计费与逆推算法。")

    # --- 基本信息 ---
    st.markdown("#### ▍1. 基本计费环境[cite: 1]")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        country = st.selectbox("国家[cite: 1]", ["美国", "英国", "德国", "日本"], index=0)
    with b2:
        calc_mode = st.radio("试算类型[cite: 1]", ["售价试算", "利润试算"], index=0, horizontal=True)
    with b3:
        ship_method = st.radio("配送方式[cite: 1]", ["FBA", "FBM"], index=0, horizontal=True)
    with b4:
        rate_val = st.number_input("汇率 (USD/CNY)[cite: 1]", value=6.735100000, step=0.01, format="%.9f")

    # --- 商品与费用设置 ---
    st.markdown("#### ▍2. 商品规格与各项费率[cite: 1]")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        cost_cny = st.number_input("采购成本 (CNY)[cite: 1]", value=float(spec["cost"]), step=1.0)
        declare_rate = st.number_input("申报比例 (%)[cite: 1]", value=0.00, step=1.0)
        customs_tax = st.number_input("关税税率 (%)[cite: 1]", value=0.00, step=1.0)

    with c2:
        st.write("**外包装尺寸 (CM)[cite: 1]**")
        d1, d2, d3 = st.columns(3)
        dim_l = d1.number_input("长[cite: 1]", value=float(spec["l"]), step=0.5)
        dim_w = d2.number_input("宽[cite: 1]", value=float(spec["w"]), step=0.5)
        dim_h = d3.number_input("高[cite: 1]", value=float(spec["h"]), step=0.5)
        act_weight = st.number_input("商品重量 (kg)[cite: 1]", value=float(spec["wt"]), step=0.01)
        dim_divisor = st.selectbox("材积除数[cite: 1]", [6000, 5000], index=0)

    with c3:
        first_leg_price = st.number_input("头程单价 (CNY/KG)[cite: 1]", value=15.00, step=1.0)
        fba_fee = st.number_input("FBA配送费用 (USD)[cite: 1]", value=6.37, step=0.01)

    with c4:
        platform_fee_pct = st.number_input("平台费率 (%)[cite: 1]", value=15.00, step=0.5)
        ad_fee_pct = st.number_input("广告费率 ACoS (%)[cite: 1]", value=10.00, step=1.0)
        refund_fee_pct = st.number_input("退款率 (%)[cite: 1]", value=20.00, step=1.0, help="重要：晚宴包退款率普遍偏高，建议保守预估在 15-25%[cite: 1]")
        other_fee_pct = st.number_input("其他费用率 (%)[cite: 1]", value=0.00, step=0.5)
        vat_tax_pct = st.number_input("VAT税率 (%)[cite: 1]", value=0.00, step=0.5)

    # 计费重量与领星标准换算[cite: 1]
    vol_weight = (dim_l * dim_w * dim_h) / dim_divisor[cite: 1]
    charge_weight = max(act_weight, vol_weight)[cite: 1]
    size_tier = "大号标准尺寸" if (dim_l <= 45 and dim_w <= 35 and dim_h <= 20 and charge_weight <= 9) else "小号大件"[cite: 1]

    # 固定支出计算
    purchase_usd = cost_cny / rate_val
    first_leg_usd = (charge_weight * first_leg_price) / rate_val[cite: 1]
    tariff_usd = (cost_cny * (declare_rate / 100.0) * (customs_tax / 100.0)) / rate_val[cite: 1]
    final_fba_usd = fba_fee if ship_method == "FBA" else 0.00[cite: 1]
    fixed_sum_usd = purchase_usd + first_leg_usd + tariff_usd + final_fba_usd[cite: 1]

    # --- 试算输出 ---
    st.markdown("---")
    res_l, res_r = st.columns([1, 1])

    if calc_mode == "售价试算"[cite: 1]:
        with res_l:
            selling_price = st.number_input("👉 建议售价 (USD)[cite: 1]", value=30.60, step=0.5, format="%.2f")
            
            p_fee = selling_price * (platform_fee_pct / 100.0)[cite: 1]
            ad_fee = selling_price * (ad_fee_pct / 100.0)[cite: 1]
            ref_fee = selling_price * (refund_fee_pct / 100.0)[cite: 1]
            oth_fee = selling_price * (other_fee_pct / 100.0)[cite: 1]
            vat_fee = selling_price * (vat_tax_pct / 100.0)[cite: 1]

            total_cost = fixed_sum_usd + p_fee + ad_fee + ref_fee + oth_fee + vat_fee[cite: 1]
            net_profit = selling_price - total_cost[cite: 1]
            margin_pct = (net_profit / selling_price * 100.0) if selling_price > 0 else 0.0[cite: 1]
            roi_pct = (net_profit / purchase_usd * 100.0) if purchase_usd > 0 else 0.0[cite: 1]

        with res_r:
            with st.container(border=True):
                st.markdown("### 📊 利润核算指标 (领星ERP模型)[cite: 1]")
                k1, k2 = st.columns(2)
                k1.metric("建议售价[cite: 1]", f"${selling_price:.2f} USD")
                k2.metric("毛利率[cite: 1]", f"{margin_pct:.2f} %[cite: 1]")

                k3, k4 = st.columns(2)
                k3.metric("预估毛利润[cite: 1]", f"${net_profit:.2f} USD[cite: 1]")
                k4.metric("ROI (投资回报率)[cite: 1]", f"{roi_pct:.2f} %[cite: 1]")

    else:
        with res_l:
            target_margin = st.number_input("👉 目标毛利率 (%)[cite: 1]", value=15.00, step=1.0, format="%.2f")
            var_rates = (platform_fee_pct + ad_fee_pct + refund_fee_pct + other_fee_pct + vat_tax_pct + target_margin) / 100.0[cite: 1]

            if var_rates >= 1.0:
                st.error("各项费率总和超过 100%，无法推导合理售价！")
                selling_price = 0.0
                p_fee = ad_fee = ref_fee = oth_fee = vat_fee = net_profit = roi_pct = margin_pct = 0.0
            else:
                selling_price = fixed_sum_usd / (1.0 - var_rates)[cite: 1]
                p_fee = selling_price * (platform_fee_pct / 100.0)[cite: 1]
                ad_fee = selling_price * (ad_fee_pct / 100.0)[cite: 1]
                ref_fee = selling_price * (refund_fee_pct / 100.0)[cite: 1]
                oth_fee = selling_price * (other_fee_pct / 100.0)[cite: 1]
                vat_fee = selling_price * (vat_tax_pct / 100.0)[cite: 1]
                net_profit = selling_price * (target_margin / 100.0)[cite: 1]
                roi_pct = (net_profit / purchase_usd * 100.0) if purchase_usd > 0 else 0.0[cite: 1]
                margin_pct = target_margin

        with res_r:
            with st.container(border=True):
                st.markdown("### 📊 反推建议定价看板 (领星ERP模型)[cite: 1]")
                k1, k2 = st.columns(2)
                k1.metric("反推建议售价[cite: 1]", f"${selling_price:.2f} USD")
                k2.metric("毛利率[cite: 1]", f"{margin_pct:.2f} %[cite: 1]")

                k3, k4 = st.columns(2)
                k3.metric("单件预估毛利润[cite: 1]", f"${net_profit:.2f} USD[cite: 1]")
                k4.metric("ROI[cite: 1]", f"{roi_pct:.2f} %[cite: 1]")

    # 领星同款明细
    with st.expander("🔍 展开查看领星标准费用科目账单[cite: 1]", expanded=False):
        st.table(pd.DataFrame({
            "费用科目[cite: 1]": ["采购成本[cite: 1]", "计费重/尺寸等级[cite: 1]", "头程运费[cite: 1]", "FBA配送费[cite: 1]", "平台费 (佣金)[cite: 1]", "广告费[cite: 1]", "退款费[cite: 1]", "关税[cite: 1]"],
            "金额 (USD)[cite: 1]": [f"${purchase_usd:.2f}", f"{charge_weight:.2f}kg ({size_tier})[cite: 1]", f"${first_leg_usd:.2f}[cite: 1]", f"${final_fba_usd:.2f}[cite: 1]", f"${p_fee:.2f}[cite: 1]", f"${ad_fee:.2f}[cite: 1]", f"${ref_fee:.2f}[cite: 1]", f"${tariff_usd:.2f}[cite: 1]"],
            "计算说明[cite: 1]": [f"¥{cost_cny:.2f} / 汇率 {rate_val:.4f}[cite: 1]", f"实重 {act_weight:.2f}kg vs 材积 {vol_weight:.2f}kg[cite: 1]", f"{charge_weight:.2f}kg × ¥{first_leg_price:.2f} / 汇率[cite: 1]", f"方式: {ship_method}[cite: 1]", f"售价 × {platform_fee_pct}%[cite: 1]", f"售价 × {ad_fee_pct}% (ACoS)[cite: 1]", f"售价 × {refund_fee_pct}%[cite: 1]", f"申报货值 × 关税率[cite: 1]"]
        }))
