import streamlit as st
import pandas as pd
import json

# Page Config: SaaS style full-width layout with custom tab title
st.set_page_config(
    page_title="TrendRadar 晚宴包选品决策与开款中台",
    page_icon="👜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SaaS-grade CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Top metric stat cards */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 8px;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-delta {
        font-size: 12px;
        font-weight: 600;
        color: #10b981;
        margin-top: 4px;
    }
    
    /* Product Showcase Card */
    .product-box {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    .product-box:hover {
        border-color: #cbd5e1;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 9px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 9999px;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-trend { background: #fee2e2; color: #ef4444; }
    .badge-blue { background: #e0f2fe; color: #0284c7; }
    .badge-purple { background: #f3e8ff; color: #9333ea; }
    .badge-green { background: #dcfce7; color: #16a34a; }
    
    /* VOC Warning Box */
    .voc-warning-card {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 6px;
        padding: 12px 14px;
        font-size: 12.5px;
        color: #78350f;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    
    /* Action Prompt Box */
    .prompt-box {
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 12px;
        color: #334155;
        font-family: monospace;
        word-break: break-all;
    }
</style>
""", unsafe_allow_html=True)

# 1. Mock Data: Real operational perspective for Amazon Bag Sellers
INIT_ITEMS = [
    {
        "id": "BAG-2026-001",
        "title": "复古丝缎纽结晚宴手拿包 (Satin Knotted Gala Clutch)",
        "silhouette": "云朵包",
        "material": "丝缎",
        "color": "勃艮第酒红",
        "occasion": "婚宴伴娘 (Wedding Guest), 毕业舞会 (Prom)",
        "trend_score": 98,
        "trend_growth": "+210% (近30天暴涨)",
        "amz_price": "$32.99 - $36.99",
        "amz_competition": "低竞争 (BSR前50仅2款在售)",
        "decision": "🔥 立即打样测款",
        "claimed_by": "运营A (Ken)",
        "status": "样品开发中",
        "voc_risks": [
            "【水渍手汗痛点】：丝缎表面极易吸附手汗形成难看水印（退货主因）。改款方案：必须要求面料厂增加特氟龙三防防泼水涂层。",
            "【提手松散风险】：纽结结构若纯靠手打容易散开。改款方案：提手内部必须车隐形暗线缝合固定。"
        ],
        "mj_prompt": "/imagine prompt: Pleated satin evening clutch, burgundy red silk, elegant knotted handle, studio product photography, clean white background, commercial handbag lighting, high-end fashion, 8k resolution --ar 4:3 --v 6.0",
        "bullet_points": "• 【UPGRADED WATER-RESISTANT SATIN】Treated with a discreet hydrophobic finish to repel accidental drink spills and finger smudges during formal evening banquets.\n• 【SECURE KNOTTED HANDLE】Reinforced internal double stitching prevents the artistic knot handle from untying even when carrying heavier essentials."
    },
    {
        "id": "BAG-2026-002",
        "title": "几何异形亚克力母贝硬壳晚宴盒 (Mother-of-Pearl Box Clutch)",
        "silhouette": "硬壳盒",
        "material": "亚克力",
        "color": "香槟天然母贝",
        "occasion": "高规格晚宴 (Black Tie Gala), 鸡尾酒会 (Cocktail)",
        "trend_score": 92,
        "trend_growth": "+165% (高端礼服博主热推)",
        "amz_price": "$39.99 - $45.99",
        "amz_competition": "中等竞争 (现有竞品评分普遍偏低 3.9分)",
        "decision": "⚠️ 改良尺寸后开款",
        "claimed_by": "未认领",
        "status": "待评审",
        "voc_risks": [
            "【容量致命硬伤】：竞品 1 星差评 60% 集中在无法装下 iPhone 15/16 Pro Max。改款方案：内部净长开模必须严格 ≥ 18.5cm（7.3英寸）。",
            "【铰链脱胶异味】：传统手工涂胶合页在夏季 FBA 易融胶脱开且化学味刺鼻。改款方案：要求工厂改用超声波铆接五金，箱内附赠吸味香氛卡。"
        ],
        "mj_prompt": "/imagine prompt: Mother of pearl acrylic box clutch, geometric luxury brass clasp, natural organic marble iridescence, evening gala minaudiere, studio lighting, hyper-realistic handbag catalog, pure white background --ar 4:3 --v 6.0",
        "bullet_points": "• 【FITS IPHONE PRO MAX WITH EASE】Specifically lengthened internal dimensions (7.4 x 4.5 in) effortlessly store large smartphones with slim cases, lipstick, and compacts.\n• 【ZERO CHEMICAL ODOR & RIVETED HINGES】Upgraded ultrasonic riveted hardware and odorless curing technology ensure zero unpleasant glue fumes out of the box."
    },
    {
        "id": "BAG-2026-003",
        "title": "复古双珠口金褶皱丝绒手腕包 (Velvet Kiss-Lock Wristlet)",
        "silhouette": "手腕包",
        "material": "丝绒",
        "color": "翡翠墨绿",
        "occasion": "圣诞派对 (Holiday Gala), 宴会晚礼服",
        "trend_score": 85,
        "trend_growth": "+88% (秋冬常青热门)",
        "amz_price": "$26.99 - $29.99",
        "amz_competition": "高竞争 (公模货多，拼差异化五金与面料手感)",
        "decision": "💡 换五金微创新",
        "claimed_by": "运营B (Sarah)",
        "status": "打样完成/核价中",
        "voc_risks": [
            "【裁剪顺逆毛反光差】：丝绒面料裁剪若方向错位，日光下两面色差严重显廉价。改款方案：跟单验货要求整批裁片统一同向顺毛。",
            "【手腕环承重脱落】：手腕金属环与绒布连接处易脱扣。改款方案：改用锌合金整体压铸圆环，打十字打枣加固。"
        ],
        "mj_prompt": "/imagine prompt: Vintage emerald green velvet evening pouch, wristlet metal ring handle, antique double-bead kiss-lock closure, soft plush velvet sheen, commercial lighting, white backdrop --ar 4:3 --v 6.0",
        "bullet_points": "• 【UNIFORM DEEP-SHEEN VELVET】Tailored with single-direction plush velvet cutting for a rich, uniform color depth under chandelier illumination.\n• 【HEAVY-DUTY WRISTLET RING】Solid zinc-alloy ring clasp with reinforced cross-stitching reliably holds up to 10 lbs without ripping fabric."
    },
    {
        "id": "BAG-2026-004",
        "title": "液态金属银抓褶信封链条手拿包 (Metallic Liquid Silver Envelope)",
        "silhouette": "信封包",
        "material": "金属镜面革",
        "color": "未来感液态银",
        "occasion": "新年派对 (New Year's Eve), 迪斯科晚宴",
        "trend_score": 89,
        "trend_growth": "+140% (欧美千禧辣妹风升温)",
        "amz_price": "$28.99 - $33.99",
        "amz_competition": "低竞争 (新兴流行色，供给偏少)",
        "decision": "🔥 立即打样测款",
        "claimed_by": "未认领",
        "status": "待评审",
        "voc_risks": [
            "【折痕掉皮痛点】：镜面 PU 在低温海运或折叠存放时易产生不可逆白痕。改款方案：必须采购防冻耐折耐刮型水性 PU 镜面料。",
            "【链条夹头发】：细蛇骨链易夹住女性长发。改款方案：标配平滑扁平 O 字防夹发链条。"
        ],
        "mj_prompt": "/imagine prompt: Liquid metallic chrome silver envelope evening clutch, gathered slouchy folds, detachable delicate chain strap, luxury Y2K aesthetic, commercial product shot, pure white backdrop --ar 4:3 --v 6.0",
        "bullet_points": "• 【CREASE-RESISTANT MIRROR FINISH】Engineered with crack-resistant flexible metallic foil PU that maintains a mirror-like shine without peeling or folding marks.\n• 【SNAG-FREE SHOULDER CHAIN】Ultra-smooth flattened O-link chain prevents frustrating hair entanglement during lively cocktail parties."
    }
]

# Initialize Session State
if "products" not in st.session_state:
    st.session_state.products = INIT_ITEMS

# ----------------- SIDEBAR: Operational Filtering & Actions -----------------
with st.sidebar:
    st.markdown("### 👜 **TrendRadar 选品工作台**")
    st.caption("版本: v2.5 Enterprise (Amazon US / EU 专属版)")
    st.markdown("---")
    
    st.markdown("#### 🎯 选品维度精准筛选")
    
    # Filter 1: Silhouette
    all_silhouettes = ["全部包型"] + list(set(p["silhouette"] for p in st.session_state.products))
    sel_silhouette = st.selectbox("包型廓形", all_silhouettes)
    
    # Filter 2: Material
    all_materials = ["全部材质"] + list(set(p["material"] for p in st.session_state.products))
    sel_material = st.selectbox("核心面料", all_materials)
    
    # Filter 3: Decision
    all_decisions = ["全部决策状态", "🔥 立即打样测款", "⚠️ 改良尺寸后开款", "💡 换五金微创新"]
    sel_decision = st.selectbox("选品评估决策", all_decisions)
    
    # Filter 4: Pipeline Status
    all_statuses = ["全部开发进度", "待评审", "样品开发中", "打样完成/核价中", "已立项下大货"]
    sel_status = st.selectbox("开款流程状态", all_statuses)
    
    st.markdown("---")
    st.markdown("#### ⚡ 团队协作与数据同步")
    
    # Feishu 1-click export
    if st.button("📋 导出当前筛选至飞书表格格式", use_container_width=True):
        tsv_rows = ["款式编码\t款式名称\t包型\t材质\t趋势得分\t建议售价\t选品决策\t防退货质检要点\t认领人\t开发进度"]
        for p in st.session_state.products:
            voc_summary = " | ".join(p["voc_risks"]).replace("\n", " ")
            tsv_rows.append(f"{p['id']}\t{p['title']}\t{p['silhouette']}\t{p['material']}\t{p['trend_score']}\t{p['amz_price']}\t{p['decision']}\t{voc_summary}\t{p['claimed_by']}\t{p['status']}")
        st.code("\n".join(tsv_rows), language="text")
        st.toast("已生成制表符 TSV，可直接复制粘贴到飞书多维表格 A1 单元格！", icon="✅")

# ----------------- MAIN VIEW: Dashboard Header & Stats -----------------
st.title("晚宴包趋势雷达与开款决策中台 (TrendRadar)")
st.markdown("面向亚马逊运营团队的**审美先导选品引擎**：提前 60-90 天挖掘 Pinterest 趋势，自动交叉比对亚马逊 1 星差评，锁定低退货率高毛利款式。")

# Top KPI Stat Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">当前追踪飙升款式</div>
        <div class="metric-value">48 <span style="font-size:16px;font-weight:normal;color:#64748b;">款</span></div>
        <div class="metric-delta">↑ 12 款较上周新增</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">平均建议售价 (ASP)</div>
        <div class="metric-value">$33.50</div>
        <div class="metric-delta" style="color:#0284c7;">毛利率预估 ≥ 68%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">已拦截潜在差评痛点</div>
        <div class="metric-value">16 <span style="font-size:16px;font-weight:normal;color:#64748b;">项</span></div>
        <div class="metric-delta" style="color:#f59e0b;">已输出防御改款方案</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">团队认领开款进度</div>
        <div class="metric-value">2 <span style="font-size:16px;font-weight:normal;color:#64748b;">款打样中</span></div>
        <div class="metric-delta" style="color:#8b5cf6;">2 款等待运营评审</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# ----------------- FILTERING LOGIC -----------------
filtered_products = st.session_state.products
if sel_silhouette != "全部包型":
    filtered_products = [p for p in filtered_products if p["silhouette"] == sel_silhouette]
if sel_material != "全部材质":
    filtered_products = [p for p in filtered_products if p["material"] == sel_material]
if sel_decision != "全部决策状态":
    filtered_products = [p for p in filtered_products if p["decision"] == sel_decision]
if sel_status != "全部开发进度":
    filtered_products = [p for p in filtered_products if p["status"] == sel_status]

# ----------------- TABS: Product Cards vs Pipeline View -----------------
tab_cards, tab_matrix, tab_pipeline = st.tabs(["📦 款式开款卡片 (视觉+质检)", "📊 运营决策速览表", "🚀 团队开款看板 (Kanban)"])

with tab_cards:
    st.caption(f"共筛选出 {len(filtered_products)} 款符合条件的晚宴包提案")
    
    for idx, prod in enumerate(filtered_products):
        with st.container():
            st.markdown(f"""
            <div class="product-box">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <span class="badge badge-trend">{prod['id']}</span>
                        <span class="badge badge-blue">{prod['silhouette']}</span>
                        <span class="badge badge-purple">{prod['material']} · {prod['color']}</span>
                        <span class="badge badge-green">{prod['decision']}</span>
                        <h3 style="margin-top:6px; margin-bottom:8px; font-size:18px; font-weight:700; color:#0f172a;">{prod['title']}</h3>
                        <p style="font-size:13px; color:#64748b; margin-bottom:6px;"><b>适用场景：</b>{prod['occasion']}</p>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:12px; color:#64748b;">Pinterest 趋势得分</div>
                        <div style="font-size:24px; font-weight:800; color:#ef4444;">{prod['trend_score']} <span style="font-size:12px;font-weight:600;">/ 100</span></div>
                        <div style="font-size:12px; color:#10b981; font-weight:600;">{prod['trend_growth']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sub-columns inside each product for operational details
            c_info, c_voc, c_actions = st.columns([1.1, 1.4, 1.2])
            
            with c_info:
                st.markdown("##### 🛒 亚马逊市场可行性诊断")
                st.markdown(f"- **建议售价 (ASP):** `{prod['amz_price']}`")
                st.markdown(f"- **竞品竞争格局:** {prod['amz_competition']}")
                st.markdown(f"- **责任认领人:** `{prod['claimed_by']}`")
                st.markdown(f"- **当前流程状态:** `{prod['status']}`")
            
            with c_voc:
                st.markdown("##### 🛡️ 亚马逊 1 星差评防御避坑卡 (VOC)")
                voc_html = "<div class='voc-warning-card'>"
                for risk in prod['voc_risks']:
                    voc_html += f"<div>{risk}</div>"
                voc_html += "</div>"
                st.markdown(voc_html, unsafe_allow_html=True)
            
            with c_actions:
                st.markdown("##### 🎨 一键开款与 Listing 交付物")
                with st.expander("🖼️ 查看 Midjourney 概念生图 Prompt", expanded=False):
                    st.code(prod['mj_prompt'], language="text")
                with st.expander("📝 查看防退货防御性 Listing 卖点", expanded=False):
                    st.code(prod['bullet_points'], language="text")
                
                # Interactive Claim / Status Update
                status_cols = st.columns(2)
                with status_cols[0]:
                    new_status = st.selectbox("更新进度", ["待评审", "样品开发中", "打样完成/核价中", "已立项下大货", "淘汰归档"], index=["待评审", "样品开发中", "打样完成/核价中", "已立项下大货", "淘汰归档"].index(prod['status']) if prod['status'] in ["待评审", "样品开发中", "打样完成/核价中", "已立项下大货", "淘汰归档"] else 0, key=f"status_{prod['id']}")
                    if new_status != prod['status']:
                        prod['status'] = new_status
                        st.rerun()
                with status_cols[1]:
                    claimer = st.text_input("认领运营", value=prod['claimed_by'], key=f"claim_{prod['id']}")
                    if claimer != prod['claimed_by']:
                        prod['claimed_by'] = claimer
                        st.rerun()
                        
            st.markdown("<hr style='margin-top:15px; margin-bottom:25px; border-color:#f1f5f9;'/>", unsafe_allow_html=True)

with tab_matrix:
    st.markdown("#### 📋 晚宴包选品决策与效益对比大表")
    table_data = []
    for p in filtered_products:
        table_data.append({
            "款式编码": p["id"],
            "款式名称": p["title"],
            "廓形": p["silhouette"],
            "主材质": p["material"],
            "颜色": p["color"],
            "趋势热度得分": p["trend_score"],
            "建议售价": p["amz_price"],
            "竞争评估": p["amz_competition"],
            "开款决策": p["decision"],
            "认领人": p["claimed_by"],
            "当前状态": p["status"]
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, height=280)
    
    # Download as Excel / CSV
    csv_bytes = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下载 CSV 选品报表 (Excel 可直接打开)",
        data=csv_bytes,
        file_name="晚宴包开款选品推荐表_TrendRadar.csv",
        mime="text/csv"
    )

with tab_pipeline:
    st.markdown("#### 🚀 团队协同开款看板 (Workflow Pipeline)")
    pipe_col1, pipe_col2, pipe_col3, pipe_col4 = st.columns(4)
    
    with pipe_col1:
        st.markdown("##### 📌 待评审 (Backlog)")
        for p in st.session_state.products:
            if p["status"] == "待评审":
                st.info(f"**{p['id']}** | {p['title'][:14]}...\n\n🔥 得分: {p['trend_score']} | 认领: `{p['claimed_by']}`")
                
    with pipe_col2:
        st.markdown("##### 🧵 样品开发中 (Sampling)")
        for p in st.session_state.products:
            if p["status"] == "样品开发中":
                st.warning(f"**{p['id']}** | {p['title'][:14]}...\n\n💰 预计: {p['amz_price']} | 责任人: `{p['claimed_by']}`")
                
    with pipe_col3:
        st.markdown("##### ⚖️ 打样完成/核价中 (Quotation)")
        for p in st.session_state.products:
            if p["status"] == "打样完成/核价中":
                st.success(f"**{p['id']}** | {p['title'][:14]}...\n\n🎯 {p['decision']} | 责任人: `{p['claimed_by']}`")
                
    with pipe_col4:
        st.markdown("##### 🚢 已立项下大货 (Launched)")
        launched_count = 0
        for p in st.session_state.products:
            if p["status"] == "已立项下大货":
                launched_count += 1
                st.markdown(f"🎉 **{p['id']}** {p['title'][:12]}...")
        if launched_count == 0:
            st.caption("暂无下大货款式")
