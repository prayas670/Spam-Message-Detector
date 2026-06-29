import re

def classify_spam_category(text):
    text_lower = text.lower()
    
    # 1. Malware Links
    # High risk terms related to downloading, installation, software updates, patches, files, attachments
    malware_keywords = [
        r'download', r'install', r'patch', r'attachment', r'attached', r'file',
        r'exe', r'zip', r'apk', r'software', r'click here to download', r'click to download',
        r'security patch', r'update software', r'update your software', r'click the link below to install',
        r'remove malware', r'adware', r'spyware', r'virus', r'trojan', r'get our app', r'download our app',
        r'install our app'
    ]
    if any(re.search(kw, text_lower) for kw in malware_keywords):
        return 'Malware Links'
        
    # 2. Fraud
    # Phishing, account compromised, billing/invoice issues, bank alerts, security alerts, shipping delays, verify credentials
    fraud_keywords = [
        r'hack', r'compromise', r'overdue', r'outstanding balance', r'unauthorized', r'verify your identity',
        r'verify identity', r'verify account', r'billing', r'invoice', r'tax', r'health insurance',
        r'medical claim', r'package', r'delivery', r'parcel', r'shipment',
        r'card ending', r'savings account', r'google account', r'microsoft account', r'whatsapp account',
        r'facebook account', r'amazon account', r'account will be banned', r'banned', r'avoid suspension',
        r'verify security', r'suspended', r'restrict', r'locked out', r'lockout', r'secure document',
        r'sign document', r'login to receive', r'verify credentials', r'verify now', r'verify here',
        r'secure now', r'legal notice', r'securely', r'reported', r'appeal', r'login was detected',
        r'fine', r'driving record', r'beneficiary', r'social media account', r'login detected',
        r'bank alert', r'suspicious activity', r'tech support', r'flagged', r'voicemail', r'unresolved fines',
        r'unverified', r'unusual activity', r'login from a new location', r'ip address', r'rebate',
        r'paypal', r'transaction', r'records', r'accident', r'voter', r'toll', r'charge', r'unpaid',
        r'closed', r'alert', r'password', r'reset', r'exposed', r'unusual', r'suspicious', r'security',
        r'activity', r'court', r'irs', r'penalties'
    ]
    if any(re.search(kw, text_lower) for kw in fraud_keywords):
        return 'Fraud'
        
    # 3. Scam
    # Get rich quick, lottery, investments, cryptocurrency, easy money, jobs requiring payment, cash prizes, sweepstakes
    scam_keywords = [
        r'investment', r'invest', r'trading', r'crypto', r'earn', r'receive', r'make', 
        r'per week', r'per day', r'per month', r'weekly', r'daily', r'monthly',
        r'peer transfer', r'cash instantly', r'lottery', r'jackpot', r'sweepstakes',
        r'won', r'win', r'winner', r'make money', r'side hustle', r'work from home', r'get rich',
        r'financial freedom', r'affiliate marketing', r'referral', r'refer friends', r'distributor',
        r'subsidy', r'subsidies', r'government grant', r'funding', r'grant', r'fund', r'trading app',
        r'bot trades', r'cash prize', r'prize money', r'awarded vip', r'millionth visitor',
        r'benefit', r'entitlement', r'profit', r'reserved', r'retirement', r'get paid', r'test apps',
        r'diploma', r'certificates', r'residency', r'valued', r'estimate', r'inherit',
        r'compensation', r'debt', r'loans', r'scholarship', r'shortlisted', r'housing scheme',
        r'loan', r'bitcoin', r'income', r'pay', r'owed', r'mortgage', r'lender', r'rate',
        r'government'
    ]
    if any(re.search(kw, text_lower) for kw in scam_keywords):
        return 'Scam'
        
    # 4. Promotional
    # Discounts, coupons, shopping, free products/trials, upgrade subscription, customer loyalty, rewards
    promo_keywords = [
        r'free', r'upgrade', r'premium', r'discount', r'coupon', r'off', r'trial', r'promo',
        r'loyalty', r'rewards', r'sample', r'supplement', r'diet pill', r'miracle pill', r'claim',
        r'order now', r'purchase', r'shop', r'save up to', r'voucher', r'gift card', r'birthday reward',
        r'personalise', r'insurance quote', r'special offer', r'limited time offer', r'buy one get one',
        r'bogo', r'sale', r'reward', r'warranty', r'renew', r'medication', r'deal', r'hotel', r'offer',
        r'prize draw', r'product tester', r'chosen to test', r'pre-selected', r'clinically proven',
        r'buy now pay later', r'zero interest', r'hair back', r'sending \d+ to your', r'mobile wallet',
        r'give', r'giving', r'prize', r'store', r'card', r'exclusive', r'watch'
    ]
    if any(re.search(kw, text_lower) for kw in promo_keywords):
        return 'Promotional'
        
    return 'Scam'
