# -*- coding: utf-8 -*-
from flask_babelex import gettext, lazy_gettext


# 开通的国家
SUPPORT_COUNTRIES = (
    (1, 'zh', gettext('China')),
    (2, 'en', gettext('USA')),
)

# 支持的币种 currencies
SUPPORT_CURRENCIES = (
    (1, 'CNY'),
    (2, 'USD'),
    (3, 'JPY'),
    (4, 'SGD'),
    (5, 'THB'),
    (6, 'KRW'),
    (7, 'SUR'),
    (8, 'PHP')
)

# 支持的语言 Language
SUPPORT_LANGUAGES = (
    (1, 'zh', '简体中文'),
    (2, 'en', 'English'),
    (3, 'th', 'Thailand'),
    (9, 'zh_TW', '繁體中文')
)

# 品牌状态
BRAND_STATUS = (
    (1, lazy_gettext('Enabled'), 'success'),
    (-1, lazy_gettext('Disabled'), 'danger')
)