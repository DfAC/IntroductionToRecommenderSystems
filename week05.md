Recommendation systems week05 - Evaluation
====

# How can we evaluate value of our recommended algorithms

* Methods
	* how far is prediction from truth (MAE, RMSE, MSE)
	* reversals count how many times a recommender system makes a very bad prediction
	* Coverage measure the number of items we got enough data to recommend it to the user
* Business
	* accuracy does not distinguish between purchases by recommender and those happening anyway
	* increase sell
	* lift, cross sales, up sales, conversions
	* serendipity, diversity
* more systematic evaluation of recommender
* evaluating predictions and recommending
	* prediction is about accuracy, decision support
	* top-N is about ranking
* how to calculate the metrics
	* what do we include/exclude
	* what about comparisons?
	* what is our baseline?
* Unary data is always different
* dead vs live evaluation
	* retrospective
		* we have a lot
		* its dead
	* live approaches
		* easy to check
		* we upset users
* [what about A/B testing?](http://recsys-qna.cs.umn.edu/#/course/1/discussion/1038)











# Rank Metrics

* prediction accuracy -  how well does recommender estimate preferences?
* decision support -  how well are we at finding good things?
	* recall
* rank accuracy - how good is our relative preferences

* [mean reciprocal mark](https://en.wikipedia.org/wiki/Mean_reciprocal_rank)
	* $\frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{rank_i}$
	* this check how good recomended do with putting good stuff first
* [separman rank corelation](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient)
	* pearson correlation of item ranks
	* we need to have ground truth
	* $\frac{\sum (i-u_i)(j-u_j)}{\sqrt{\sum (i-u_i)}\sqrt{\sum (j-u_j)}}$ where i is recomended rank and j is current rank
	 	* in case of tie we will assign average rank so order is not important
	 * it punishes all misplaces equally
	 * it is not so commonly used
	 * in recommender we care more about high level items than ones lover down the list
* [normalised discounted cumulative gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)
	* this solves a problem as we discount utility by the position (fron/top more importaht)
	* we normalise by total achievable utility
	* [Kaggle uses it](https://www.kaggle.com/wiki/NormalizedDiscountedCumulativeGain)
	```
	$DCG(R) =  \sum u(i)d(i)$ where d(i) discount, making items down list less important for ex $d(i)=\frac{}{max(1,log_2i)}$ or [half life approach](https://en.wikipedia.org/wiki/Half-life) $d(i) = \frac{1}{2^{\frac{i-1}{\alpha-1}}}$
	$nDCG(R) = frac{nDCG(R)}{DCG(R_{perferct})}$

	```
	* it is becoming very common now
* pares
	* we compare how much of all possible pairs are in proper order

# Hidden data evaluations

* fallacy of this hidden data evaluation
* algorythm will get punished if it returns items I haven't seen yet
* Netflix challenge - it was supposed to improved RMSE
	* this does not solve the problem
	* you want to use whole scale for things that matters not for counting failure
* you are aiming for most popular item here, which is not the best approach
	* user might have bought it anyway
* magic solution here is **testing with users**
* those metricks are useful to weed out poor models and poor data
* does your methodology sustain your

# more metrics

* relevance of individual predictions
* focusing on specific goals - business for example
* how can we make sure that we cover other interests
* coverage
	* we need to remove similar units
	* for ex use categories
	* calculate pairwise similarities for the n items
	* if we show only few items, augment this with different recommender (user-user or non-personal ones)
* diversity - remove items which are too similar to items in the top-n already
	* people prefer lists that are not accurate but allow for wider diversity of things
	* introduce clustering and show only top from each cluster
	* don't turn away customers by showing them narrow answers
	* if recommender have low diversity replace items with lower ranked but more diverse items
* serendipity
	* probability of surprise prediction
	* need to be relevant
	* downgrade most popular items to promote less-know items
	* only recommended top important books if you love them
* make it interesting for user
	* good business case here
	* note that some business approach might still require to still show most important books

# Experiment protocols

* we want to estimate recommender quality
	* user based evaluation
	* business needs
* inspired by
	* machine learning
	* information retrieval
* types
	* hidden data
		* hold out one of k run it k-1 times
			* most popular are k= 5-10
	* cross validation
		* multiple hold-outs
		* prevents artefacts
	* information retrieval
		* compare against expert knowledge
		* the same as k-fold but we are also going to subset user preferences
		* we will test how well we predict the withhold data (test data)
			* we might consider using last 10 instead of random
			* its not realistic - we can't have data after user selection normally!
		* use RMSE, MAE, nDCG per user
	* using log data
		* for unary data (clicks)


# unary data

* implicit feedback
* it is positive only
	* we can't use it for negative examples
	* most of the time we dont have negative data
	* people played song but we dont know what songs they didnt played
* metrics
	* Precision/Recall/MAP
	* MRR
		* get pushed down
	* % at before rank
	* nDCG
* some solutions
	* synthesise data to create negative data
	* limit domain of recommendations
		* we limit chances of finding item that user didnt looked for before
	* one sided classification
		* testing only on positive data
* offline evaluation is problematic

# User centered evaluation

* it compliment offline evaluation we discussed before
* we need it for whole picture
* need to understand difference between retrieval and recommendation
* user behaviour is complex
* types
	* user logs
	* pool, surveys, focus groups
		* don't confuse selling with information gathering
	* experiments (labs)
		* controlled

# Interviews

## Neal Lathia

* how your data behaviour over time
* experience improvement over time
* results has to change otherwise ppl will not see recomender to work proerly
* improve diversity
	* swap between algorithms
	* it is much more difficult for attacker to sucessfuly spoof the system

# Nava Tintarev - explanations

* how can we explain how recommended system works ?
* connect of transparency
	* concept of trust don't always work here
* sometimes conversation with system is useful
* there are always trade offs


# Assignment 4: Evaluation

The goal of this assignment is for you to get experience thinking through the appropriate metrics and evaluation designs for recommender systems.



## Problem 1

You are responsible for a recommender system for an e-commerce site that has **three slots** in which to recommend products at check-out time. In general, you are most interested in whether people buy additional products based on the recommendations, and you will be measuring sales and lift when your system is live, but you want an offline measure to help determine which potential recommenders are worth trying online.

A few other details: this is a domain where people do occasionally re-purchase items, but not frequently. Most regular customers visit between once a week and once every three months. The site has complete details on all previous purchases, and has customer ratings for about 5% of the purchased items. Also, the site does a pretty good job recommending to new customers based on demographics and overall popularity, so you are focused on **finding recommenders that take advantage of information learned from customers who have already purchased several items**. Which of the following evaluation plans/metrics seems best?


* Top-n precision evaluation. In this plan we’ll use all customers who have at least 10 product purchases, and measure the top-3 precision of recommendations using a 5-fold cross-validation against a random 80% training/20% test set. We measure as a “hit” anything withheld from the test set. We will identify the best few algorithm candidates based on highest top-3 precision.

<del>

* RMSE-based accuracy evaluation. In this plan, we will take any customers who have at least 10 different prior ratings and measure the accuracy of predictions from the recommender using the leave-one-out method. We’ll average over all predicted ratings, and will identify the best few algorithm candidates based on lowest RMSE.

* Spearman rank correlation evaluation. In this plan, we’ll use all customers who have at least 10 product purchases, compute a recommendation list (using and 80/20 random training/test data set and five-fold cross validation), and measure the Spearman correlation between the between the withheld items and the recommedation list. We will identify the best few algorithms based on the highest Spearman correlation.

* Diversity and Serendipity evaluation. In this plan, we’ll use all customers who have at least 10 product purchases, compute a recommendation list for each customer (using their entire rating/purchase set), and measure the diversity and popularity of the top-3 recommendations. We’ll take a balanced measure of diversity and inverse popularity (50% each), and identify the

</del>

## Problem 2

Which of the following is a situation in which Mean Absolute Error is a reasonable choice as a metric for evaluating recommender performance?

* You are running a travel-related recommendation site where users can look for hotels and restaurants (somewhat like TripAdvisor). For a given hotel or restaurant, you have a collection of data, including user ratings (lots of them), tags, written reviews and objective attributes (e.g., swimming pool, 24 hour restaurant). When displaying an item, the system shows a predicted rating (in this case personalized according to the user’s profile, unlike TripAdvisor’s average). Some usage is through search for specific places (e.g., Holiday Inn Hong Kong Kowloon), and search for category/location (e.g., Hotel swimming pool Paris). But about 80% of accesses go directly to a particular hotel or restaurant’s page driven from search engines such as Google and Bing. The recommender is used both to produce the predicted ratings and as part of producing a ranked list of results for internal searches (where it is merged together with a search algorithm that measures quality of match to the search terms). Your site benefits both from visitors (through ads) and from booking referral payments.

<del>
* You are running a streaming music site with a recommender inside that selects music to provide listeners with a personalized music listening experience (somewhat like Pandora). The basic interface is very small, it shows the name of the song and artist, and has controls that allow the user to click on a star (for favorite) or on an X (for don’t play this again). It also allows users to click a forward arrow (skip to next song). Your goal is to have users enjoy the music enough to continue listening to the site (which is paid for by advertisements, which the user cannot skip).

* You are running an online news site that presents users with an on-screen newspaper (somewhat like Google news). The site places articles into categories, the first of which is “top stories for you,” and the others are traditional news categories (local news, world news, sports, business, etc.). The contents of each category are selected by the recommender, as is the order of presentation of items. Each items is displayed as a headline, and the first story in each category also has a few sentences from the start of the story. User feedback is entirely implicit -- users either read the full article or don’t. Your goal is to have high site usage, as the site also contains advertisements.

* You are running an e-commerce site for a shoe store (somewhat like Zappos). Your site has a large set of shoes, with structured product data for each (colors, materials, sizes, etc.). It also has user purchase data and user rating data. While some customers mostly visit the site to re-purchase shoes they already own that have worn out, **most of the profit comes from people with large shoe collections who regularly buy new pairs of shoes**. Your responsibility is a recommender system that sends out a periodic e-mail to the store’s best customers suggesting items for purchase and offering a premium if the user makes a purchase within a certain time period. A typical e-mail would have pictures and descriptions of four pairs of shoes, along with a promotion such as a free travel shoe bag if placing an order for more than $100 before November 15th. Your site is a pure commerce site -- your revenue comes from sales. The goal for the e-mail program is to generate sales, though it is not considered important whether the customers buy the recommended items, or end up choosing to buy other items. **All that matters is how much they buy**.
</del>

# Problem 3

Which of the following is a situation in which it would be most useful to tune the recommender using a metric such as the receiver operating characteristic -- specifically, tuning the algorithm to find the right trade-off between [true positive and false positive rates](https://en.wikipedia.org/wiki/Sensitivity_and_specificity)?

* You are running a streaming music site with a recommender inside that selects music to provide listeners with a personalized music listening experience (somewhat like Pandora). The basic interface is very small, it shows the name of the song and artist, and has controls that allow the user to click on a star (for favorite) or on an X (for don’t play this again). It also allows users to click a forward arrow (skip to next song). Your goal is to have users enjoy the music enough to continue listening to the site (which is paid for by advertisements, which the user cannot skip).


# Problem 4

All of these situations are ones where it would make sense to test different recommenders empirically through A/B tests or other field tests. In which situation is it LEAST LIKELY that you could get useful data by asking users which set of outputs they prefer? In other words, in which situation are users least likely to know whether the recommender is actually achieving its goals?

* You are running an e-commerce site for a shoe store (somewhat like Zappos). Your site has a large set of shoes, with structured product data for each (colors, materials, sizes, etc.). It also has user purchase data and user rating data. While some customers mostly visit the site to re-purchase shoes they already own that have worn out, most of the profit comes from people the large shoe collections who regularly buy new pairs of shoes. Your responsibility is a recommender system that sends out a periodic e-mail to the store’s best customers suggesting items for purchase and offering a premium if the user makes a purchase within a certain time period. A typical e-mail would have pictures and descriptions of four pairs of shoes, along with a promotion such as a free travel shoe bag if placing an order for more than $100 before November 15th. Your site is a pure commerce site -- your revenue comes from sales. The goal for the e-mail program is to generate sales, though it is not considered important whether the customers buy the recommended items, or end up choosing to buy other items. All that matters is how much they buy.

# Problem 5

We have argued that the real proof of a recommender system is in the usage, and that offline evaluation has serious problems. At the same time, there are many situations where offline evaluation does make sense. Which of these is a valid reason for carrying out off-line metric-based evaluation rather than a live user study of a recommender?
<del>
a. The recommender may not yet exist yet, but there is data that can be used to pre-test the idea of the recommender.

b. The recommender designer wants to test a wide variety of alternative recommenders, at least to narrow them down to a few candidates that can be user tested.

c. Neither (a) nor (b)
</del>
d. Both (a) and (b)

# Problem 6

Which of the following is a valid objection to the validity of offline evaluation using metrics such as MAE, top-n Precision, or nDCG?

a. The offline metrics only assess the ability to “recommend” items that have already been consumed or rated. Real recommenders should usually be suggesting new items not already known to the user. Hence, something with low offline metrics might acually be better at finding new items of interest.

<del>
b. The offline metrics depend completely on the scale of the data being presented. For instance if you change a rating scale from 5 points to 100 points, the MAE will increase by a factor of 20.

c. Offline metrics come in different groups. Some measure accuracy. Some address decision correctness. Some look at rank. That means that we can’t tell if any metric is relevant for any particular recommender system.

d. All of the above objections are valid.
</del>