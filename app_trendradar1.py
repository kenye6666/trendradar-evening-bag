import streamlit as st
import pandas as pd

# ==============================================================================
# 页面全局设置 (适合多栏款式对比与数据看板的宽屏布局)
# ==============================================================================
st.set_page_config(
    page_title="亚马逊晚宴包趋势雷达与选品测算工作台",
    page_icon="👜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 内置款式发掘数据库 (包含款式图、≤3星差评VOC深度归因、1688以图搜款与规格)
# ==============================================================================
TREND_PRODUCTS = [
    {
        "id": "YB260640",
        "title": "法式复古缎面褶皱晚宴手拿包 (Pleated Satin Clutch)",
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&auto=format&fit=crop&q=80",
        "occasion": "婚礼晚宴 (Wedding Guest)",
        "material": "丝缎 (Satin)",
        "silhouette": "云朵/手拿 (Cloud/Pouch)",
        "color": "香槟金 / 香槟母贝",
        "trend_score": 96,
        "weekly_growth": "+320%",
        "selling_point": "Pinterest当季搜索飙升爆款，高密度缎面光泽搭配手工抓褶垂坠感，小巧吸睛且适配多种礼服。",
        "voc_analysis": {
            "critical_rating_ratio": "17.5% (≤3星真实评论占比)",
            "pain_points": [
                {"issue": "面料沾水/手汗留深色水印", "severity": "高危", "desc": "缎面面料无防水处理，酒会现场水渍或手汗极易留下明显水印，客户无法清洁导致三星及以下差评。"},
                {"issue": "内部净长极限无法容纳 Pro Max 手机", "severity": "致命", "desc": "两端抓褶设计挤压了内部实用空间，带保护壳的 6.7 英寸大屏手机无法正常拉紧合拢。"},
                {"issue": "金属肩带夹扯头发与真丝裙摆", "severity": "严重", "desc": "赠送的普通蛇骨链存在细微毛刺咬合，走动时极易钩损昂贵真丝礼服或扯头发。"}
            ],
            "action_advice": "要求供应商在面料上增加环保三防涂层（防泼水防污）；内部净有效长度拉长至19.5cm以上；配链必须升级为无缝圆角扁链并出厂进行丝袜擦拭测试。"
        },
        "supplier_1688": {
            "avg_price_cny": 29.00,
            "shop_name": "广州市白云区雅尚皮具制造厂",
            "shop_rating": "4.8分 (6年诚信通工厂)",
            "moq": "2个起批 (支持混批与一件起发)",
            "search_link": "https://s.1688.com/youyuan/index.htm?tab=imageSearch",
            "specs_desc": "31.00 × 19.50 × 7.00 CM | 净重 0.27 kg | 配防尘绒布袋"
        },
        "default_specs": {
            "cost_cny": 29.00,
            "length_cm": 31.00,
            "width_cm": 19.50,
            "height_cm": 7.00,
            "weight_kg": 0.27
        }
    },
    {
        "id": "YB260641",
        "title": "勃艮第酒红丝绒法棍晚宴包 (Burgundy Velvet Bag)",
        "image_url": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=600&auto=format&fit=crop&q=80",
        "occasion": "毕业舞会 (Prom)",
        "material": "丝绒 (Velvet)",
        "silhouette": "手腕包 (Wristlet)",
        "color": "勃艮第酒红 (Burgundy)",
        "trend_score": 91,
        "weekly_growth": "+210%",
        "selling_point": "复古秋冬红丝绒质感，配异形巴洛克纽结金属扣，优雅高级，尤其适合欧美毕业舞会与节日庆典。",
        "voc_analysis": {
            "critical_rating_ratio": "14.8% (≤3星真实评论占比)",
            "pain_points": [
                {"issue": "工厂顺逆毛裁片导致明显反光阴阳色", "severity": "高危", "desc": "同一只包正面与侧面包片顺逆毛方向不一致，强光照射下色泽断层严重，买家直呼廉价感。"},
                {"issue": "金属手腕环连接处脱线", "severity": "严重", "desc": "受力点仅采用单道明线缝合，放入手机及随身小物件后承受拉力不足导致织物开裂。"}
            ],
            "action_advice": "裁剪环节严格规范定型单向走绒；金属环衔接织物处内侧增加加厚织带加固与双道回针加固处理。"
        },
        "supplier_1688": {
            "avg_price_cny": 24.50,
            "shop_name": "义乌市蝶彩箱包有限公司",
            "shop_rating": "4.6分 (4年金牌供应商)",
            "moq": "5个起批",
            "search_link": "https://s.1688.com/youyuan/index.htm?tab=imageSearch",
            "specs_desc": "28.00 × 18.00 × 6.00 CM | 净重 0.22 kg"
        },
        "default_specs": {
            "cost_cny": 24.50,
            "length_cm": 28.00,
            "width_cm": 18.00,
            "height_cm": 6.00,
            "weight_kg": 0.22
        }
    },
    {
        "id": "YB260642",
        "title": "异形亚克力母贝硬壳宴会盒 (Acrylic Minaudiere Box)",
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80",
        "occasion": "黑领结正装宴 (Black Tie)",
        "material": "亚克力 (Acrylic)",
        "silhouette": "硬壳盒 (Minaudiere)",
        "color": "天然母贝白 (Pearl White)",
        "trend_score": 87,
        "weekly_growth": "+175%",
        "selling_point": "硬朗建筑线条感搭配天然珍珠贝母光泽，金边框立体锁扣，在海外晚宴中出镜率极高。",
        "voc_analysis": {
            "critical_rating_ratio": "25.2% (≤3星真实评论占比，高退货预警品类)",
            "pain_points": [
                {"issue": "严重刺鼻的化学胶水气味", "severity": "致命", "desc": "出厂直接套密封胶袋，胶水未彻底挥发，海外买家拆开后充斥刺鼻异味无法直接带去派对。"},
                {"issue": "合页松动与硬壳撞击易开裂", "severity": "高危", "desc": "物流剧烈震动易造成合页螺丝脱落或四角暗裂。"}
            ],
            "action_advice": "出厂前强制经过72小时通风散味工序，包装内标配除味活性炭及香氛卡；采用加厚珍珠棉独立抗震礼盒包装。"
        },
        "supplier_1688": {
            "avg_price_cny": 38.00,
            "shop_name": "东莞市精美塑胶五金工艺品厂",
            "shop_rating": "4.9分 (8年专精特新)",
            "moq": "10个起批",
            "search_link": "https://s.1688.com/youyuan/index.htm?tab=imageSearch",
            "specs_desc": "20.00 × 12.00 × 5.50 CM | 净重 0.45 kg | 防震泡沫开模盒"
        },
        "default_specs": {
            "cost_cny": 38.00,
            "length_cm": 20.00,
            "width_cm": 12.00,
            "height_cm": 5.50,
            "weight_kg": 0.45
        }
    }
]

# ==============================================================================
# 侧边栏：由运营自由限定的定向筛选窗口 (纯可视化选择，无代码)
# ==============================================================================
with st.sidebar:
    st.header("🎯 选品款式定向筛选")
    st.caption("由亚马逊运营限定具体场景、材质与廓形，精准定位垂直细分爆款。")

    filter_occasions = st.multiselect(
        "限定目标场合 (Occasion)",
        options=["全部场合", "婚礼晚宴 (Wedding Guest)", "毕业舞会 (Prom)", "黑领结正装宴 (Black Tie)", "鸡尾酒派对 (Cocktail)"],
        default=["全部场合"]
    )

    filter_materials = st.multiselect(
        "限定面料材质 (Material)",
        options=["全部材质", "丝缎 (Satin)", "丝绒 (Velvet)", "亚克力 (Acrylic)", "水钻满镶 (Rhinestone)", "珍珠串珠 (Pearl)"],
        default=["全部材质"]
    )

    filter_silhouettes = st.multiselect(
        "限定包型廓形 (Silhouette)",
        options=["全部廓形", "云朵/手拿 (Cloud/Pouch)", "手腕包 (Wristlet)", "硬壳盒 (Minaudiere)", "信封手拿包 (Envelope)"],
        default=["全部廓形"]
    )

    st.divider()
    st.markdown("#### ⚙️ 选品数据配置")
    show_1688_info = st.checkbox("展示 1688 以图搜款货源与比价", value=True)
    min_trend_score = st.slider("最低趋势指数门槛", min_value=60, max_value=100, value=80, step=1)

# 数据筛选计算
matched_products = []
for item in TREND_PRODUCTS:
    match_occ = "全部场合" in filter_occasions or item["occasion"] in filter_occasions
    match_mat = "全部材质" in filter_materials or item["material"] in filter_materials
    match_sil = "全部廓形" in filter_silhouettes or item["silhouette"] in filter_silhouettes
    match_score = item["trend_score"] >= min_trend_score
    if match_occ and match_mat and match_sil and match_score:
        matched_products.append(item)

# ==============================================================================
# 主界面：三大核心业务模块
# ==============================================================================
st.title("👜 亚马逊晚宴包智能选品与利润测算工作台")
st.markdown("集 **海外趋势发掘对比**、**1688以图搜款货源直通**、**≤3星差评(VOC)防退货归因** 与 **领星ERP同款利润试算** 于一体的运营工作台。")

tab_gallery, tab_voc, tab_calc = st.tabs([
    "🖼️ 款式发掘与多维对比 (带图)",
    "🛡️ 亚马逊 ≤3星差评(VOC)深度防退货看板",
    "💰 亚马逊利润试算器 (领星ERP模型)"
])

# ------------------------------------------------------------------------------
# 模块 1：款式发掘与画册对比 (带图片输出与1688以图搜款)
# ------------------------------------------------------------------------------
with tab_gallery:
    st.subheader(f"共发掘到 {len(matched_products)} 款符合条件的趋势款式")

    if not matched_products:
        st.info("💡 当前筛选组合下暂无匹配款式，请在左侧侧边栏放宽场景、材质或降低门槛。")
    else:
        num_cols = min(len(matched_products), 3)
        cols = st.columns(num_cols)

        for i, prod in enumerate(matched_products):
            with cols[i % num_cols]:
                with st.container(border=True):
                    # 图片可视化输出，方便运营一眼对比
                    st.image(prod["image_url"], use_container_width=True, caption=f"款式编号: {prod['id']}")
                    st.markdown(f"**{prod['title']}**")

                    c1, c2 = st.columns(2)
                    c1.caption(f"场合: {prod['occasion']}")
                    c2.caption(f"材质: {prod['material']}")

                    st.metric("趋势指数", f"{prod['trend_score']} 分", delta=prod["weekly_growth"])
                    st.write(f"✨ **买点：** {prod['selling_point']}")

                    if show_1688_info:
                        st.markdown("---")
                        st.markdown("**🛒 1688 以图搜款货源行情：**")
                        s_info = prod["supplier_1688"]
                        st.write(f"• **平均采购价：** :red[**¥{s_info['avg_price_cny']:.2f}**]")
                        st.write(f"• **推荐工厂：** {s_info['shop_name']}")
                        st.caption(f"认证: {s_info['shop_rating']} | 起订: {s_info['moq']}")
                        st.caption(f"参考规格: {s_info['specs_desc']}")

                        # 直达1688以图搜款页面
                        st.link_button(
                            label="🔍 打开1688以图搜款找同款货源",
                            url=s_info["search_link"],
                            use_container_width=True
                        )

# ------------------------------------------------------------------------------
# 模块 2：亚马逊 ≤3星差评 (VOC) 深度防退货看板
# ------------------------------------------------------------------------------
with tab_voc:
    st.subheader("🛡️ 亚马逊竞品 ≤3星差评归因与工厂工艺改良卡")
    st.caption("全面抓取分析竞品 Listing 的 1星、2星与3星评价。3星以下评论能最真实反映产品做工落差、材质隐患与高退货根源。")

    chosen_prod = st.selectbox(
        "选择要进行差评避坑分析的款式：",
        options=TREND_PRODUCTS,
        format_func=lambda x: f"[{x['id']}] {x['title']}"
    )

    if chosen_prod:
        v_data = chosen_prod["voc_analysis"]
        v_col_img, v_col_content = st.columns([1, 2])

        with v_col_img:
            st.image(chosen_prod["image_url"], use_container_width=True, caption="分析标的款式")
            st.error(f"⚠️ 竞品类目平均负面评价率: {v_data['critical_rating_ratio']}")
            st.markdown("#### 📋 给工厂/供应链的整改要求：")
            st.info(v_data["action_advice"])

        with v_col_content:
            st.markdown("#### 🔍 核心痛点与缺陷集中分布 (≤3星评价归因)")
            for p_item in v_data["pain_points"]:
                with st.expander(f"🔴 [{p_item['severity']}] {p_item['issue']}", expanded=True):
                    st.write(f"**买家集中抱怨现象：** {p_item['desc']}")
                    st.caption("💡 运营防守策略：在亚马逊 Listing 首图、尺寸透视图及 A+ 页面中做前置说明，主动化解买家过度预期。")

# ------------------------------------------------------------------------------
# 模块 3：亚马逊利润试算器 (领星ERP模型像素级还原)
# ------------------------------------------------------------------------------
with tab_calc:
    st.subheader("💰 亚马逊利润试算 (领星ERP计费模型)")
    st.caption("按照领星ERP标准的计费方式测算产品定价与毛利，支持输入框自定数值并即时双向联动试算。")

    # 快捷载入款式的实测尺寸与1688采购价
    active_prod = st.selectbox(
        "快捷同步所选款式的尺寸与采购价：",
        options=TREND_PRODUCTS,
        format_func=lambda x: f"【{x['id']}】{x['title']} (采购价: ¥{x['supplier_1688']['avg_price_cny']})"
    )
    defaults = active_prod["default_specs"]

    st.markdown("---")

    # --- 基本信息 ---
    st.markdown("#### ▍基本信息[cite: 1]")
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        country = st.selectbox("国家[cite: 1]", ["美国", "英国", "德国", "日本"], index=0)
        calc_template = st.selectbox("试算模板[cite: 1]", ["美国海运-箱包电器0306", "美东空派快捷模板", "欧洲铁运模板"], index=0)
    with b_col2:
        shipping_channel = st.radio("配送方式[cite: 1]", ["FBA", "FBM"], index=0, horizontal=True)
        pricing_mode = st.radio("试算类型[cite: 1]", ["售价试算", "利润试算"], index=0, horizontal=True)
    with b_col3:
        rate_val = st.number_input("汇率 (USD/CNY)[cite: 1]", value=6.735100000, step=0.01, format="%.9f")
    with b_col4:
        st.write("")

    # --- 商品信息 ---
    st.markdown("#### ▍商品信息[cite: 1]")
    st.caption(f"品名: evening-bag {active_prod['id']}  |  SKU: {active_prod['id']}[cite: 1]")

    c_col1, c_col2, c_col3, c_col4 = st.columns(4)

    with c_col1:
        cost_cny = st.number_input("采购成本 (CNY)[cite: 1]", value=float(defaults["cost_cny"]), step=1.0)
        declare_rate = st.number_input("申报货值比例 (%)[cite: 1]", value=0.00, step=1.0, help="申报货值 = 采购成本 × 申报货值比例[cite: 1]")
        customs_tax_rate = st.number_input("关税税率 (%)[cite: 1]", value=0.00, step=1.0)

    with c_col2:
        st.write("**商品外包装尺寸 (CM)[cite: 1]**")
        dim1, dim2, dim3 = st.columns(3)
        dim_l = dim1.number_input("长[cite: 1]", value=float(defaults["length_cm"]), step=0.5)
        dim_w = dim2.number_input("宽[cite: 1]", value=float(defaults["width_cm"]), step=0.5)
        dim_h = dim3.number_input("高[cite: 1]", value=float(defaults["height_cm"]), step=0.5)

        actual_weight = st.number_input("商品重量 (kg)[cite: 1]", value=float(defaults["weight_kg"]), step=0.01)
        dim_divisor = st.selectbox("材积除数[cite: 1]", [6000, 5000], index=0)

    with c_col3:
        first_leg_type = st.radio("头程单价[cite: 1]", ["自定义单价", "引用头程物流"], index=0, horizontal=True)
        first_leg_unit_price = st.number_input("头程单价 (CNY/KG)[cite: 1]", value=15.00, step=1.0)
        product_category = st.selectbox("商品类型[cite: 1]", ["非服装类商品", "服装类商品"], index=0)
        custom_fba_fee = st.number_input("FBA费用 (USD)[cite: 1]", value=6.37, step=0.01)

    with c_col4:
        platform_commission_rate = st.number_input("平台费率 (%)[cite: 1]", value=15.00, step=0.5)
        ad_fee_rate = st.number_input("广告费率 (%)[cite: 1]", value=10.00, step=1.0)
        refund_fee_rate = st.number_input("退款率 (%)[cite: 1]", value=20.00, step=1.0)
        other_fee_rate = st.number_input("其他费用率 (%)[cite: 1]", value=0.00, step=0.5)
        vat_fee_rate = st.number_input("VAT税率 (%)[cite: 1]", value=0.00, step=0.5)

    # 计费重量与尺寸等级换算 (与领星截图一致：31×19.5×7 / 6000 = 0.705kg 进位为 0.71kg[cite: 1])
    volumetric_weight = (dim_l * dim_w * dim_h) / dim_divisor[cite: 1]
    chargeable_weight = max(actual_weight, volumetric_weight)[cite: 1]
    size_tier_label = "大号标准尺寸" if (dim_l <= 45 and dim_w <= 35 and dim_h <= 20 and chargeable_weight <= 9) else "小号大件"[cite: 1]

    # --- 费用计算基础部分 ---
    # 采购成本 (USD)
    purchase_usd = cost_cny / rate_val
    # 头程费用 (USD) = 计费重量(kg) * 头程单价(CNY) / 汇率[cite: 1]
    first_leg_usd = (chargeable_weight * first_leg_unit_price) / rate_val[cite: 1]
    # 关税 (USD) = 采购成本 * (申报比例 / 100) * (关税税率 / 100) / 汇率[cite: 1]
    tariff_usd = (cost_cny * (declare_rate / 100.0) * (customs_tax_rate / 100.0)) / rate_val[cite: 1]
    # FBA费用[cite: 1]
    fba_shipping_usd = custom_fba_fee if shipping_channel == "FBA" else 0.00[cite: 1]
    # 固定成本总和 (不随售价改变的硬支出)
    fixed_cost_sum_usd = purchase_usd + first_leg_usd + tariff_usd + fba_shipping_usd[cite: 1]

    # --- 试算核心推导 ---
    st.markdown("---")
    res_box_left, res_box_right = st.columns([1, 1])

    if pricing_mode == "售价试算"[cite: 1]:
        with res_box_left:
            selling_price_input = st.number_input("建议售价 (USD)[cite: 1]", value=30.60, step=0.1, format="%.2f")

            # 随售价变动的费用
            platform_fee_usd = selling_price_input * (platform_commission_rate / 100.0)[cite: 1]
            ad_fee_usd = selling_price_input * (ad_fee_rate / 100.0)[cite: 1]
            refund_fee_usd = selling_price_input * (refund_fee_rate / 100.0)[cite: 1]
            other_fee_usd = selling_price_input * (other_fee_rate / 100.0)[cite: 1]
            vat_fee_usd = selling_price_input * (vat_fee_rate / 100.0)[cite: 1]

            total_expenses_usd = fixed_cost_sum_usd + platform_fee_usd + ad_fee_usd + refund_fee_usd + other_fee_usd + vat_fee_usd[cite: 1]
            gross_profit_usd = selling_price_input - total_expenses_usd[cite: 1]
            gross_profit_margin = (gross_profit_usd / selling_price_input * 100.0) if selling_price_input > 0 else 0.0[cite: 1]
            roi_value = (gross_profit_usd / purchase_usd * 100.0) if purchase_usd > 0 else 0.0[cite: 1]

        with res_box_right:
            with st.container(border=True):
                st.markdown("### 📊 利润核算指标 (领星ERP模型)[cite: 1]")
                k1, k2 = st.columns(2)
                k1.metric("建议售价[cite: 1]", f"${selling_price_input:.2f} USD")
                k2.metric("毛利率[cite: 1]", f"{gross_profit_margin:.2f} %[cite: 1]")

                k3, k4 = st.columns(2)
                k3.metric("毛利润[cite: 1]", f"${gross_profit_usd:.2f} USD[cite: 1]")
                k4.metric("ROI[cite: 1]", f"{roi_value:.2f} %[cite: 1]")

    else:
        with res_box_left:
            target_margin_input = st.number_input("目标毛利率 (%)[cite: 1]", value=15.00, step=0.5, format="%.2f")

            # 逆推公式: 售价 * (1 - 佣金% - 广告% - 退款% - 其他% - VAT% - 目标毛利%) = 固定成本和[cite: 1]
            rate_sum = (platform_commission_rate + ad_fee_rate + refund_fee_rate + other_fee_rate + vat_fee_rate + target_margin_input) / 100.0[cite: 1]

            if rate_sum >= 1.0:
                st.error("各项费率总和超过 100%，无法推导合理售价！")
                derived_selling_price = 0.0
                platform_fee_usd = ad_fee_usd = refund_fee_usd = other_fee_usd = vat_fee_usd = 0.0
                gross_profit_usd = 0.0
                roi_value = 0.0
                gross_profit_margin = 0.0
            else:
                derived_selling_price = fixed_cost_sum_usd / (1.0 - rate_sum)[cite: 1]
                platform_fee_usd = derived_selling_price * (platform_commission_rate / 100.0)[cite: 1]
                ad_fee_usd = derived_selling_price * (ad_fee_rate / 100.0)[cite: 1]
                refund_fee_usd = derived_selling_price * (refund_fee_rate / 100.0)[cite: 1]
                other_fee_usd = derived_selling_price * (other_fee_rate / 100.0)[cite: 1]
                vat_fee_usd = derived_selling_price * (vat_fee_rate / 100.0)[cite: 1]
                gross_profit_usd = derived_selling_price * (target_margin_input / 100.0)[cite: 1]
                roi_value = (gross_profit_usd / purchase_usd * 100.0) if purchase_usd > 0 else 0.0[cite: 1]
                gross_profit_margin = target_margin_input

        with res_box_right:
            with st.container(border=True):
                st.markdown("### 📊 定价逆推指标 (领星ERP模型)[cite: 1]")
                k1, k2 = st.columns(2)
                k1.metric("反推建议售价[cite: 1]", f"${derived_selling_price:.2f} USD")
                k2.metric("毛利率[cite: 1]", f"{gross_profit_margin:.2f} %[cite: 1]")

                k3, k4 = st.columns(2)
                k3.metric("预估毛利润[cite: 1]", f"${gross_profit_usd:.2f} USD[cite: 1]")
                k4.metric("ROI[cite: 1]", f"{roi_value:.2f} %[cite: 1]")

    # --- 领星同款费用科目明细拆解表 ---
    with st.expander("🔍 查看领星ERP费用明细账单拆解[cite: 1]", expanded=True):
        fee_summary_df = pd.DataFrame({
            "费用科目[cite: 1]": [
                "采购成本[cite: 1]", "计费重量 / 尺寸等级[cite: 1]", "头程费用[cite: 1]", 
                "FBA费用[cite: 1]", "平台费 (佣金)[cite: 1]", "广告费[cite: 1]", 
                "退款费[cite: 1]", "关税费用[cite: 1]", "其他费用[cite: 1]", "VAT费用[cite: 1]"
            ],
            "金额 (USD)[cite: 1]": [
                f"${purchase_usd:.2f}",
                f"{chargeable_weight:.2f} kg ({size_tier_label})[cite: 1]",
                f"${first_leg_usd:.2f} USD[cite: 1]",
                f"${fba_shipping_usd:.2f} USD[cite: 1]",
                f"${platform_fee_usd:.2f} USD[cite: 1]",
                f"${ad_fee_usd:.2f} USD[cite: 1]",
                f"${refund_fee_usd:.2f} USD[cite: 1]",
                f"${tariff_usd:.2f} USD[cite: 1]",
                f"${other_fee_usd:.2f} USD[cite: 1]",
                f"${vat_fee_usd:.2f} USD[cite: 1]"
            ],
            "计费公式与对应说明[cite: 1]": [
                f"¥{cost_cny:.2f} / 汇率 {rate_val:.4f}[cite: 1]",
                f"实重 {actual_weight:.2f}kg vs 材积重 {volumetric_weight:.2f}kg (材积系数 {dim_divisor}) 取大者[cite: 1]",
                f"计费重 {chargeable_weight:.2f}kg × ¥{first_leg_unit_price:.2f} / 汇率[cite: 1]",
                f"配送方式: {shipping_channel}[cite: 1]",
                f"售价 × {platform_commission_rate:.2f}%[cite: 1]",
                f"售价 × {ad_fee_rate:.2f}% (ACoS)[cite: 1]",
                f"售价 × {refund_fee_rate:.2f}%[cite: 1]",
                f"申报货值 × 关税率 {customs_tax_rate:.2f}%[cite: 1]",
                f"售价 × {other_fee_rate:.2f}%[cite: 1]",
                f"售价 × {vat_fee_rate:.2f}%[cite: 1]"
            ]
        })
        st.table(fee_summary_df)
