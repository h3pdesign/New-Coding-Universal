from pocket_tagger import PocketTagger

tagger = PocketTagger(
    gcloud_credentials_file="/Users/h3p/pocket-tagging-2588febe36bc.json",
    consumer_key="113137-db3d33cc63e9b9b4b028856",
    access_token="a044bef6-695d-c21d-3111-f6b3a6",
)


# %%

# Initialize PocketTagger with GCloud and Pocket API Credentials
tagger = PocketTagger(
    gcloud_credentials_file="gcloud_credentials_file.json",
    consumer_key="113137-db3d33cc63e9b9b4b028856",
    access_token="a044bef6-695d-c21d-3111-f6b3a6",
)

# Check https://getpocket.com/developer/docs/v3/retrieve for additional list of options you can pass for retrieving pocket list
articles = tagger.get_articles_from_api(count=10, offset=10, detailType="complete")

# Alternatively you can load the articles from file if you saved them previously using save_articles_to_file
# articles = tagger.get_articles_from_file("20190621.json")
# Generate tags for each article
articles_with_tags = tagger.get_tags_for_articles(articles)

# Save the articles with tags to file. You can use this file to verify it looks good before running the final step to tag the articles.
tagger.save_articles_to_file(
    today.strftime("%Y%m%d-with-tags.json"), articles_with_tags
)

# You can skip this step if you want to do a dry run. Verify the tags in the file we generated in the previous step.
tagger.add_tags_to_articles(articles_with_tags)
