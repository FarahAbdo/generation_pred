import json

class RealEstateInvestmentAnalyzer:
    def __init__(self):
        self.contexts = {
            'tower': {
                'districts': {
                    'النرجس': {'base_price': 8000, 'premium': 1.2},
                    'الملقا': {'base_price': 8500, 'premium': 1.3},
                    'القيروان': {'base_price': 7500, 'premium': 1.1},
                    'الياسمين': {'base_price': 7800, 'premium': 1.25},
                    'العارض': {'base_price': 7000, 'premium': 1.0},
                    'حطين': {'base_price': 9000, 'premium': 1.35}
                },
                'build_ratios': {
                    'ground_floor': 0.70,
                    'first_floor': 0.80,
                    'top_attachment': 0.75,
                    'alternative_ratios': {
                        'ground_floor': 0.50,
                        'first_floor': 0.65,
                        'top_attachment': 0.75
                    }
                },
                'unit_sizes': {
                    'residential': {'min': 80, 'max': 250},
                    'commercial': {'min': 50, 'max': 100}
                }
            },
            'hotel': {
                'districts': {
                    'النرجس': {'base_price': 9000, 'premium': 1.3},
                    'الملقا': {'base_price': 9500, 'premium': 1.4},
                    'القيروان': {'base_price': 8500, 'premium': 1.15},
                    'الياسمين': {'base_price': 8800, 'premium': 1.2},
                    'العارض': {'base_price': 8000, 'premium': 1.05},
                    'حطين': {'base_price': 10000, 'premium': 1.45}
                },
                'build_ratios': {
                    'ground_floor': 0.80,
                    'first_floor': 0.85,
                    'top_attachment': 0.80,
                    'alternative_ratios': {
                        'ground_floor': 0.60,
                        'first_floor': 0.75,
                        'top_attachment': 0.80
                    }
                },
                'unit_sizes': {
                    'hotel_room': {'min': 25, 'max': 60}
                }
            },
            'administrative_building': {
                'districts': {
                    'النرجس': {'base_price': 7500, 'premium': 1.2},
                    'الملقا': {'base_price': 8000, 'premium': 1.3},
                    'القيروان': {'base_price': 7000, 'premium': 1.1},
                    'الياسمين': {'base_price': 7800, 'premium': 1.25},
                    'العارض': {'base_price': 6500, 'premium': 1.0},
                    'حطين': {'base_price': 8500, 'premium': 1.35}
                },
                'build_ratios': {
                    'ground_floor': 0.65,
                    'first_floor': 0.75,
                    'top_attachment': 0.70,
                    'alternative_ratios': {
                        'ground_floor': 0.35,
                        'first_floor': 0.45,
                        'top_attachment': 0.70
                    }
                },
                'unit_sizes': {
                    'office': {'min': 100, 'max': 300}
                }
            },
            'residential_compound': {
                'districts': {
                    'النرجس': {'base_price': 5700, 'premium': 1.2},
                    'الملقا': {'base_price': 6000, 'premium': 1.3},
                    'القيروان': {'base_price': 5500, 'premium': 1.1},
                    'الياسمين': {'base_price': 5800, 'premium': 1.25},
                    'العارض': {'base_price': 5200, 'premium': 1.0},
                    'حطين': {'base_price': 6400, 'premium': 1.35}
                },
                'build_ratios': {
                    'ground_floor': 0.65,
                    'repeated_floor': 0.75,
                    'top_floor': 0.70,
                    'alternative_ratios': {
                        'ground_floor': 0.50,
                        'repeated_floor': 0.70,
                        'top_floor': 0.75
                    }
                },
                'unit_sizes': {
                    'residential_unit': {'min': 100, 'max': 180}
                }
            },
            'villa': {
                'districts': {
                    'النرجس': {'base_price': 11000, 'premium': 1.4},
                    'الملقا': {'base_price': 11500, 'premium': 1.45},
                    'القيروان': {'base_price': 10500, 'premium': 1.3},
                    'الياسمين': {'base_price': 11200, 'premium': 1.35},
                    'العارض': {'base_price': 9500, 'premium': 1.2},
                    'حطين': {'base_price': 12000, 'premium': 1.5}
                },
                'build_ratios': {
                    'ground_floor': 0.80,
                    'first_floor': 0.85,
                    'top_attachment': 0.90,
                    'alternative_ratios': {
                        'ground_floor': 0.65,
                        'first_floor': 0.75,
                        'top_attachment': 0.85
                    }
                },
                'unit_sizes': {
                    'villa': {'min': 200, 'max': 500}
                }
            },
            'commercial_mall': {},
            'villas': {}
        }


    def generate_investment_report(self, land_area, district, num_floors, context_type):
        # Validate inputs
        context = self.contexts.get(context_type)
        if not context:
            raise ValueError(f"Context '{context_type}' not found")

        district_data = context['districts'].get(district)
        if not district_data:
            raise ValueError(f"District '{district}' not found")

        # Initialize variables
        effective_total_build_area = 0
        total_revenue = 0
        gross_profit = 0
        gross_margin = 0
        total_annual_rent = 0
        net_annual_rent = 0
        rental_roi = 0
        construction_cost = 0
        total_investment = 0
        annual_rent_per_sqm = 0

        # Common calculations
        base_price_per_sqm = district_data['base_price']
        premium = district_data['premium']
        purchase_price_per_sqm = base_price_per_sqm * premium
        total_land_cost = land_area * purchase_price_per_sqm

        # Get build ratios based on number of floors
        build_ratios = context['build_ratios']
        if num_floors > 4:
            build_ratios = build_ratios['alternative_ratios']

        # Calculate effective building area based on context type
        if context_type == 'tower':
            effective_total_build_area = self._calculate_tower_area(land_area, build_ratios, num_floors)
        elif context_type == 'hotel':
            effective_total_build_area = self._calculate_hotel_area(land_area, build_ratios, num_floors)
        elif context_type == 'administrative_building':
            effective_total_build_area = (
                (land_area * build_ratios['ground_floor']) +
                (land_area * build_ratios['first_floor'] * (num_floors - 2)) +
                (land_area * build_ratios['first_floor'] * build_ratios['top_attachment'])
            )
        elif context_type == 'residential_compound':
            building_area = (land_area * 0.40) / 4  # 40% building area divided into 4 buildings
            effective_total_build_area = (
                (building_area * build_ratios['ground_floor']) +
                (building_area * build_ratios['repeated_floor'] * (num_floors - 2)) +
                (building_area * build_ratios['top_floor'])
            ) * 4  # Multiply by 4 buildings
        elif context_type == 'villa':
            effective_total_build_area = (
                (land_area * build_ratios['ground_floor']) +
                (land_area * build_ratios['first_floor'] * (num_floors - 2)) +
                (land_area * build_ratios['first_floor'] * build_ratios['top_attachment'])
            )
        elif context_type == 'villas':
            villa_area = 300  # standard villa size
            effective_land_building_area = land_area * 0.40
            num_villas = int(effective_land_building_area // villa_area)
            
            single_villa_area = (
                (villa_area * build_ratios['ground_floor']) +
                (villa_area * build_ratios['first_floor'] * (num_floors - 2)) +
                (villa_area * build_ratios['top_attachment'])
            )
            effective_total_build_area = single_villa_area * num_villas
        elif context_type == 'commercial_mall':
            effective_total_build_area = (
                (land_area * build_ratios['ground_floor']) +
                (land_area * build_ratios['first_floor'] * (num_floors - 2)) +
                (land_area * build_ratios['first_floor'] * build_ratios['top_attachment'])
            )

        # Calculate costs (common for all types)
        construction_cost_per_sqm = 1400
        construction_cost = effective_total_build_area * construction_cost_per_sqm
        additional_costs = {
            "design": 200000,
            "legal_and_admin": 150000,
            "site_development": 100000
        }
        total_additional_costs = sum(additional_costs.values())
        total_investment = total_land_cost + construction_cost + total_additional_costs

        # Calculate revenues and profits based on context type
        if context_type == 'tower':
            sale_price_per_sqm = base_price_per_sqm * 1.5
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.08
        elif context_type == 'hotel':
            sale_price_per_sqm = base_price_per_sqm * 1.6
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.12
        elif context_type == 'administrative_building':
            sale_price_per_sqm = base_price_per_sqm * 1.4
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.09
        elif context_type == 'residential_compound':
            sale_price_per_sqm = base_price_per_sqm * 1.3
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.07
        elif context_type == 'villa':
            sale_price_per_sqm = base_price_per_sqm * 1.7
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.06
        elif context_type == 'villas':
            sale_price_per_sqm = base_price_per_sqm * 1.65
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.07
        elif context_type == 'commercial_mall':
            sale_price_per_sqm = base_price_per_sqm * 1.8
            total_revenue = effective_total_build_area * sale_price_per_sqm
            annual_rent_per_sqm = base_price_per_sqm * 0.15

        # Common calculations for all types
        if total_revenue > 0:
            gross_profit = total_revenue - total_investment
            gross_margin = (gross_profit / total_investment) * 100 if total_investment > 0 else 0
        
        if annual_rent_per_sqm:
            total_annual_rent = effective_total_build_area * annual_rent_per_sqm
            operating_expenses = total_annual_rent * 0.2
            net_annual_rent = total_annual_rent - operating_expenses
            rental_roi = (net_annual_rent / total_investment) * 100 if total_investment > 0 else 0

        return self._generate_report_by_type(
            context_type,
            district,
            land_area,
            effective_total_build_area,
            total_land_cost,
            construction_cost,
            total_investment,
            total_revenue,
            gross_profit,
            gross_margin,
            total_annual_rent,
            net_annual_rent,
            rental_roi
        )

    def _calculate_tower_area(self, land_area, build_ratios, num_floors):
        effective_ground_area = land_area * build_ratios['ground_floor']
        effective_first_floor_area = land_area * build_ratios['first_floor']
        effective_top_attachment_area = effective_first_floor_area * build_ratios['top_attachment']
        return effective_ground_area + (effective_first_floor_area * (num_floors - 2)) + effective_top_attachment_area

    def _calculate_hotel_area(self, land_area, build_ratios, num_floors):
        effective_ground_area = land_area * build_ratios['ground_floor']
        effective_first_floor_area = land_area * build_ratios['first_floor']
        effective_top_attachment_area = effective_first_floor_area * build_ratios['top_attachment']
        return effective_ground_area + (effective_first_floor_area * (num_floors - 2)) + effective_top_attachment_area

    def _generate_report_by_type(self, context_type, district, land_area, effective_area, 
                                total_land_cost, construction_cost, total_investment,
                                total_revenue, gross_profit, gross_margin,
                                total_annual_rent, net_annual_rent, rental_roi):
        # Generate base report
        base_report = {
            "مقدمة": f"دراسة استثمارية شاملة لمشروع {context_type} في {district}",
            "العنوان": f"تطوير مشروع {context_type} في {district}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": f"تحليل استثمار تطوير {context_type} في {district}",
                "تفاصيل_المشروع": {
                    "الموقع": district,
                    "مساحة_الأرض": f"{land_area:,.2f} متر مربع",
                    "مساحة_البناء_الفعالة": f"{effective_area:,.2f} متر مربع"
                },
                "التكاليف": {
                    "تكلفة_الأرض": f"{total_land_cost:,.2f} ريال",
                    "تكلفة_البناء": f"{construction_cost:,.2f} ريال",
                    "إجمالي_الاستثمار": f"{total_investment:,.2f} ريال"
                },
                "الإيرادات": {
                    "إيرادات_البيع": f"{total_revenue:,.2f} ريال",
                    "الربح_الإجمالي": f"{gross_profit:,.2f} ريال",
                    "هامش_الربح": f"{gross_margin:.2f}%",
                    "الإيجار_السنوي": f"{total_annual_rent:,.2f} ريال",
                    "صافي_الإيجار_السنوي": f"{net_annual_rent:,.2f} ريال",
                    "العائد_على_الاستثمار": f"{rental_roi:.2f}%"
                }
            }
        }

        # Generate context-specific reports
        if context_type == 'villa':
            return {**base_report, **self._generate_villa_report(
                land_area, effective_area, total_investment, total_revenue, 
                gross_profit, gross_margin, total_annual_rent, net_annual_rent, rental_roi
            )}
        elif context_type == 'commercial_mall':
            return {**base_report, **self._generate_mall_report(
                land_area, effective_area, total_investment, total_revenue,
                gross_profit, gross_margin, total_annual_rent, net_annual_rent, rental_roi
            )}
        elif context_type == 'villas':
            # Get build ratios and costs from the instance
            build_ratios = self.contexts.get('villa', {}).get('build_ratios', {})
            construction_cost_per_sqm = 1400  # Default construction cost
            additional_costs = {
                "design": 200000,
                "legal_and_admin": 150000,
                "site_development": 100000
            }
            total_additional_costs = sum(additional_costs.values())
            
            # Calculate purchase price per sqm
            district_data = self.contexts.get('villa', {}).get('districts', {}).get(district, {})
            base_price = district_data.get('base_price', 0)
            premium = district_data.get('premium', 1)
            purchase_price_per_sqm = base_price * premium
            
            # Calculate number of floors (assuming it's passed to the generate_investment_report method)
            num_floors = getattr(self, 'num_floors', 3)  # Default to 3 if not set
            
            villas_report = {
                "تفاصيل_إضافية": {
                    "نوع_المشروع": "تطوير سكني فردي",
                    "معايير_التطوير": {
                        "نسبة_البناء_الفعالة_على_الأرض": "40%",
                        "مساحة_الأرض_الفعالة_للبناء": f"{land_area * 0.4:,.2f} متر مربع",
                        "مساحة_الفيلا": "300 متر مربع",
                        "نسبة_البناء_للدور_الأرضي": f"{build_ratios.get('ground_floor', 0.65)*100}%",
                        "نسبة_البناء_للأدوار_المتكررة": f"{build_ratios.get('first_floor', 0.75)*100}%",
                        "نسبة_البناء_للملحق_العلوي": f"{build_ratios.get('top_attachment', 0.70)*100}%",
                        "مساحة_البناء_الفعالة": f"{effective_area:,.2f} متر مربع",
                        "عدد_الفلل_المقترح": f"{int((land_area * 0.4) // 300)}",
                    },
                    "توقعات_التمويل": {
                        "تكلفة_شراء_الأرض": {
                            "تكلفة_الشراء_لكل_متر_مربع": f"{purchase_price_per_sqm:,.2f} ريال سعودي",
                            "التكلفة_الكلية": f"{total_land_cost:,.2f} ريال سعودي"
                        },
                        "تكاليف_البناء": {
                            "تكلفة_البناء_لكل_متر_مربع": f"{construction_cost_per_sqm:,.2f} ريال سعودي",
                            "مجموع_تكاليف_البناء": f"{construction_cost:,.2f} ريال سعودي",
                            "التكاليف_الإضافية": additional_costs,
                            "المجموع": f"{construction_cost + total_additional_costs:,.2f} ريال سعودي"
                        }
                    }
                }
            }
            return {**base_report, **villas_report}
        else:
            return base_report

    def _generate_villa_report(self, land_area, effective_area, total_investment, 
                            total_revenue, gross_profit, gross_margin,
                            total_annual_rent, net_annual_rent, rental_roi):
        return {
            "تفاصيل_إضافية": {
                "نوع_المشروع": "تطوير سكني فردي",
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": "65%",
                    "نسبة_البناء_للأدوار_المتكررة": "75%",
                    "نسبة_البناء_للملحق_العلوي": "70%"
                }
            }
        }

    def _generate_mall_report(self, land_area, effective_area, total_investment,
                            total_revenue, gross_profit, gross_margin,
                            total_annual_rent, net_annual_rent, rental_roi):
        return {
            "تفاصيل_إضافية": {
                "نوع_المشروع": "مول تجاري",
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": "80%",
                    "نسبة_البناء_للأدوار_المتكررة": "85%",
                    "نسبة_البناء_للملحق_العلوي": "80%"
                }
            }
        }
    # elif context_type == 'villas' :
    #           # Build the JSON response
    #     data = {
    #     "مقدمة": "هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع فلل فاخر في حي النرجس بالرياض...",
    #     "العنوان": "دراسة حالة استثمارية لتطوير فلل في حي النرجس بالرياض",
    #     "تقرير_تحليل_الاستثمار": {
    #         "مقدمة": "تحليل استثماري مفصل...",
    #         "تفاصيل_المشروع": {
    #             "الموقع": location,
    #             "مساحة_الأرض_الإجمالية": f"{total_land_area} متر مربع",
    #             "نوع_المشروع": "تطوير سكني فردي",
    #             "تنظيمات_التخطيط": "3 طوابق"
    #         },
    #         "معايير_التطوير": {
    #             "نسبة_البناء_الفعالة_على_الأرض": "40%",
    #             "مساحة_الأرض_الفعالة_للبناء": f"{effective_land_building_area} متر مربع",
    #             "مساحة_الفيلا": f"{villa_area} متر مربع",
    #             "نسبة_البناء_للدور_الأرضي": "65%",
    #             "نسبة_البناء_للأدوار_المتكررة": "75%",
    #             "نسبة_البناء_للملحق_العلوي": "70%",
    #             "مساحة_البناء_الفعالة_للدور_الأرضي": f"{effective_building_area_ground} متر مربع",
    #             "مساحة_البناء_الفعالة_للأدوار_المتكررة": f"{effective_building_area_repeated} متر مربع",
    #             "مساحة_البناء_الفعالة_للملحق_العلوي": f"{effective_building_area_upper} متر مربع",
    #             "نتيجة_مساحة_البناء_الفعالة": f"{total_effective_building_area} متر مربع",
    #             "عدد_الفلل_المقترح": f"{num_villas}",
    #             "مجموع_مساحة_البناء_الفعالة_للكومباوند": f"{total_compound_building_area} متر مربع"
    #         },
    #         "توقعات_التمويل": {
    #             "تكلفة_شراء_الأرض": {
    #                 "تكلفة_الشراء_لكل_متر_مربع": f"{land_cost_per_sqm} ريال سعودي",
    #                 "التكلفة_الكلية": f"{total_land_cost} ريال سعودي"
    #             },
    #             "تكاليف_البناء": {
    #                 "تكلفة_البناء_لكل_متر_مربع": f"{building_cost_per_sqm} ريال سعودي",
    #                 "مجموع_تكاليف_البناء": f"{total_building_cost} ريال سعودي",
    #                 "التكاليف_الإضافية": additional_costs,
    #                 "المجموع": f"{total_building_cost + total_additional_costs} ريال سعودي"
    #             },
    #             "الاستثمار_الكلي": f"{total_investment} ريال سعودي",
    #             "توقعات_الإيرادات_من_البيع": {
    #                 "سعر_البيع_لكل_متر_مربع": f"{selling_price_per_sqm} ريال سعودي",
    #                 "إيرادات_محتملة_من_البيع": f"{potential_revenue} ريال سعودي",
    #                 "هامش_الربح_الإجمالي": f"{gross_profit_margin} ريال سعودي",
    #                 "نسبة_هامش_الربح_الإجمالي": f"{gross_profit_margin_ratio:.2f}%"
    #             },
    #             "توقعات_الإيرادات_من_الإيجار": {
    #                 "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"{annual_rent_per_sqm} ريال سعودي",
    #                 "الإيجار_السنوي_الكلي": f"{total_annual_rent} ريال سعودي",
    #                 "النفقات_التشغيلية": f"{operational_expenses} ريال سعودي",
    #                 "صافي_الإيجار_السنوي": f"{net_annual_rent} ريال سعودي",
    #                 "عائد_الاستثمار_من_الإيجار": f"{roi_rental:.2f}%"
    #             }
    #         }
    #     },
    #     "ملخص_تنفيذي": "التطوير المقترح يمثل استثمارًا استراتيجيًا مربحًا في ظل ظروف السوق الحالية..."
    # }
          
    #     elif context_type == 'commerical_mall':
    #         data = {
    #     "مقدمة": "تحليل استثماري لتطوير مشروع مميز في حي النرجس بالرياض. المشروع يتضمن تطوير مول تجاري فاخر مع دراسة الإيرادات والتكاليف.",
    #     "العنوان": f"دراسة جدوى تطوير مول تجاري في {project_type}",
    #     "تقرير_تحليل_الاستثمار": {
    #         "مقدمة": "هذا التحليل يستعرض الجوانب المالية والفنية لمشروع مول تجاري في حي النرجس بالرياض.",
    #         "تفاصيل_المشروع": {
    #             "الموقع": "حي النرجس، الرياض",
    #             "مساحة_الأرض_الإجمالية": f"{total_area:,} متر مربع",
    #             "نوع_المشروع": "مول تجاري",
    #             "تنظيمات_التخطيط": f"يسمح ببناء حتى {max_floors} طوابق"
    #         },
    #         "معايير_التطوير": {
    #             "نسبة_البناء_للدور_الأرضي": floor_building_ratio,
    #             "نسبة_البناء_للأدوار_المتكررة": first_floor_ratio,
    #             "نسبة_البناء_للملحق_العلوي": upper_extension_ratio,
    #             "الطوابق_المقترحة": max_floors,
    #             "مساحة_البناء_الفعالة_للدور_الأرضي": building_area_ground_floor,
    #             "مساحة_البناء_الفعالة_للمتكرر": building_area_repeat_floors,
    #             "مساحة_البناء_الفعالة_للملحق_العلوي": building_area_upper_extension,
    #             "مساحة_البناء_الفعالة_للأدوار_المتكررة": effective_building_area_repeat,
    #             "نتيجة_مساحة_البناء_الفعالة": total_effective_building_area,
    #             "معامل_البناء": building_coefficient
    #         },
    #         "توقعات_التمويل": {
    #             "تكلفة_شراء_الأرض": {
    #                 "تكلفة_الشراء_لكل_متر_مربع": cost_per_sqm_land,
    #                 "التكلفة_الكلية": total_land_cost,
    #                 "نتيجة_التكلفة_الكلية": f"{total_land_cost:,} ريال سعودي"
    #             },
    #             "تكاليف_البناء": {
    #                 "تكلفة_البناء_لكل_متر_مربع": cost_per_sqm_construction,
    #                 "مجموع_تكاليف_البناء": total_construction_cost,
    #                 "نتيجة_مجموع_تكاليف_البناء": f"{total_construction_cost:,} ريال سعودي",
    #                 "التكاليف_الإضافية": {
    #                     "تصميم_معماري": architectural_design_cost,
    #                     "قانوني_وإداري": legal_and_admin_cost,
    #                     "تنسيق_الموقع": site_coordination_cost
    #                 },
    #                 "المجموع": total_building_cost,
    #                 "نتيجة_المجموع": f"{total_building_cost:,} ريال سعودي"
    #             },
    #             "الاستثمار_الكلي": total_investment,
    #             "نتيجة_الاستثمار_الكلي": f"{total_investment:,} ريال سعودي",
    #             "توقعات_الإيرادات_من_البيع": {
    #                 "إيرادات_محتملة_من_البيع": expected_sale_revenue,
    #                 "نتيجة_الإيرادات_المحتملة_من_البيع": f"{expected_sale_revenue:,} ريال سعودي",
    #                 "هامش_الربح_الإجمالي": gross_profit_margin,
    #                 "نتيجة_هامش_الربح_الإجمالي": f"{gross_profit_margin:,} ريال سعودي",
    #                 "نسبة_هامش_الربح_الإجمالي": gross_profit_margin_percentage
    #             },
    #             "توقعات_الإيرادات_من_الإيجار": {
    #                 "الإيجار_السنوي_المتوقع_لكل_متر_مربع": expected_annual_rent_per_sqm,
    #                 "الإيجار_السنوي_الكلي": total_annual_rent,
    #                 "نتيجة_الإيجار_السنوي_الكلي": f"{total_annual_rent:,} ريال سعودي",
    #                 "النفقات_التشغيلية": operational_expenses,
    #                 "نتيجة_النفقات_التشغيلية": f"{operational_expenses:,} ريال سعودي",
    #                 "صافي_الإيجار_السنوي": net_annual_rent,
    #                 "نتيجة_صافي_الإيجار_السنوي": f"{net_annual_rent:,} ريال سعودي",
    #                 "عائد_الاستثمار_من_الإيجار": rent_investment_return
    #             }
    #         },
    #         "تقييم_المخاطر": {
    #             "تقلبات_السوق": "متوسطة - يواجه سوق العقارات في الرياض تقلبات دورية.",
    #             "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
    #             "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
    #         },
    #         "اعتبارات_استراتيجية": {
    #             "اتجاهات_السوق": "يشهد سوق العقارات في الرياض حالياً اتجاهاً تصاعدياً.",
    #             "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية.",
    #             "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية."
    #         },
    #         "ملخص_تنفيذي": "يمثل التطوير المقترح استثمارًا جذابًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات.",
    #         "توصيات": "المضي قدماً في الاستحواذ والتطوير مع مراقبة مستمرة للأسواق."
    #     }
    # }

    #     else :
    #         data = {
    #         "مقدمة": f"دراسة استثمارية شاملة لمشروع {context_type} في {district}.",
    #         "العنوان": f"تطوير مشروع {context_type} في {district}",
    #         "تقرير_تحليل_الاستثمار": {
    #             "مقدمة": f"تحليل استثمار تطوير {context_type} في {district} يشمل كافة الجوانب المالية والفنية.",
    #             "تكاليف_الأراضي": total_land_cost,
    #             "مساحة_البناء_الفعالة": effective_total_build_area,
    #             "التكلفة_البناء": construction_cost,
    #             "التكاليف_الإضافية": total_additional_costs,
    #             "إجمالي_الاستثمار": total_investment,
    #             "إيرادات_المبيعات": total_revenue,
    #             "الربح_الخام": gross_profit,
    #             "هامش_الربح": gross_margin,
    #             "إيرادات_الإيجار_السنوية": total_annual_rent,
    #             "إيرادات_الإيجار_السنوية_الصافية": net_annual_rent,
    #             "العائد_على_الاستثمار_الإيجاري": rental_roi
    #         }
    #     }

# Example Usage:
real_estate_analyzer = RealEstateInvestmentAnalyzer()
result = real_estate_analyzer.generate_investment_report(5000, "النرجس", 5, "villa")
print(result)
