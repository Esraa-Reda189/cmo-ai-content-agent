from agent.content_agent import run_content_agent
from agent.schemas import ContentRequest

def print_result(name: str, result):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

    if result.subject_line:
        print(f"📧 Subject Line: {result.subject_line}")

    if result.platform_rules:
        print(f"📋 Platform Rules Applied: {result.platform_rules.get('best_practices','')}")

    print(f"\n📝 Generated Content:\n{result.generated_content}")

    if result.variations:
        print(f"\n🔀 Variations Found: {len(result.variations)}")
        for v in result.variations:
            print(f"  [{v.variation_id}]: {v.content[:100]}...")

    if result.hashtags:
        print(f"\n#️⃣  Hashtags: {result.hashtags}")

    if result.seo:
        print(f"\n🔍 SEO Data:")
        print(f"  Keywords: {result.seo.keywords}")
        print(f"  Meta: {result.seo.meta_description}")
        print(f"  Title: {result.seo.suggested_title}")

    print(f"\n📊 Char Count: {result.char_count} | Within Limit: {result.within_limit}")

if __name__ == "__main__":

    req1 = ContentRequest(
        content_type="social_media_post",
        brand_name="FreshBrew",
        industry="Coffee & Beverages",
        target_audience="Young professionals aged 22-35",
        tone="casual",
        platform="instagram",
        topic_or_offer="New oat milk latte launch 20% off",
        cta="Order now via link in bio",
    )

    req2 = ContentRequest(
        content_type="email_campaign",
        brand_name="FreshBrew",
        industry="Coffee & Beverages",
        target_audience="Existing subscribers",
        tone="professional",
        platform="email",
        topic_or_offer="Loyalty rewards program launch",
        cta="Join the rewards club",
    )

    req3 = ContentRequest(
        content_type="promotional_message",
        brand_name="FreshBrew",
        industry="Coffee & Beverages",
        target_audience="Coffee lovers",
        tone="inspirational",
        topic_or_offer="Flash sale 30% off for 24 hours",
        cta="Shop now",
    )

    for name, req in [
        ("INSTAGRAM POST", req1),
        ("EMAIL CAMPAIGN", req2),
        ("PROMOTIONAL MESSAGE", req3)
    ]:
        result = run_content_agent(req)
        print_result(name, result)
