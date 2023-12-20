# Scraping Flight Data Using Python

## The nerdy way to plan your next weekend trip

[![Gregor Hesse](https://miro.medium.com/v2/resize:fill:88:88/2*rkeInJy6WYwTtqPPI8UXRA.jpeg)

](https://medium.com/@ghesse85?source=post_page-----e71b97e859d3--------------------------------)[![Towards Data Science](https://miro.medium.com/v2/resize:fill:48:48/1*CJe3891yB1A1mzMdqemkdg.jpeg)

](https://towardsdatascience.com/?source=post_page-----e71b97e859d3--------------------------------)

[Gregor Hesse](https://medium.com/@ghesse85?source=post_page-----e71b97e859d3--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F9a960a1cc5dd&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fscraping-flight-data-using-python-e71b97e859d3&user=Gregor+Hesse&userId=9a960a1cc5dd&source=post_page-9a960a1cc5dd----e71b97e859d3---------------------post_header-----------)

Published in[

Towards Data Science

](https://towardsdatascience.com/?source=post_page-----e71b97e859d3--------------------------------)·4 min read·Apr 23, 2019

\--

1

Listen

Share

Let’s say we want to plan our next weekend trip. Plan is to go either to Milan or Madrid. Point is we really don’t care, we’re just looking for the best option. It’s a bit like the German soccer player Andy Möller once said: «_Milan or Madrid, as long as it is Italy_».

In a first step, we just look for a flight like we would usually do. For this example we use [_Kayak_](http://www.kayak.com). Once we’ve entered our search criteria and set a few additional filters like «_Nonstop_», we can see that interestingly the URL in our browser has adjusted accordingly

We can actually dissect this URL into different parts: origin, destination, startdate, endate and a suffix that tells [_Kayak_](http://www.kayak.com) to look only for direct connections and to sort the results by price.

Now the general idea is to get the information we want (e.g. price, departure and arrival times) from the underlying html code of the website. To do this, we mainly rely on two packages. The first one is _selenium_, which basically controls your browser and automatically opens the website. The second one is _Beautiful Soup_, which helps us to reshape the messy HTML code into a more structured and readable format. From this «soup» we can later easily get the tasty bites we’re looking for.

So let’s get started. First we need to set up s*elenium*. For this, we need to download a browser driver, e.g. [_ChromeDriver_](http://chromedriver.chromium.org/downloads) (make sure it corresponds to your installed version of Chrome), which we have to put in the same folder as our Python code. Now we load a few packages and tell _selenium_ that we want to use _ChromeDriver_ and let it open our URL from above.

Once the website has loaded, we need to find out how we can access the information that is relevant for us. Let’s take e.g. the departure time, using the inspect feature of our browser, we can see that the 8:55pm departure time is wrapped in a span with a class called «_depart-time base-time_».

If we now pass the website’s html code to _BeautifulSoup_, we can specifically search for the classes we’re interested in. The results can then be extracted with a simple loop. Since for each search result we get a set of two departure times, we also need to reshape the results into logical departure-arrival time pairs.

We use a similar approach for the price. However, when inspecting the price element, we can see that [_Kayak_](http://www.kayak.com) likes to use different classes for its price information. Therefore, we have to use a regular expression in order to capture all cases. Also the price itself is further wrapped up, that’s why we need to use a few additional steps to get to it.

Now, we put everything into a nice dataframe and get

And this is pretty much it. We have scraped and put into shape all the information that was tangled up in the html code of our initial flight. The heavy lifting is done.

To make things a bit more convenient, we can now wrap our code from above into a function and call that function by using different destination and starting day combinations for our three-day journey. When sending several requests, [_Kayak_](http://www.kayak.com) might think from time to time that we’re a bot (and who can blame them), the best way to take care of this is by constantly changing the browser’s user agent and also by waiting a bit between the requests. Our **entire code** would then look like this:

Once we have specified all combinations and scraped the respective data, we can nicely visualize our results using a heatmap from _seaborn_

So it’s decided. Next stop: Madrid! For just $108 it is the cheapest option of the three weekends we picked in September. Looking forward to eating some delicious tapas.
