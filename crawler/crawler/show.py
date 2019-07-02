import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("books.db")
curr = conn.cursor()

review_counts = [review_count[0] for review_count in curr.execute("SELECT review_count FROM books_tb")]
prices = [price[0] for price in curr.execute("SELECT price FROM books_tb")]

for i in range(len(review_counts)):
    for j in range(len(prices)):
        if review_counts[j] < review_counts[i]:
            review_counts[i], review_counts[j] = review_counts[j], review_counts[i]
            prices[i], prices[j] = prices[j], prices[i]

plt.plot(review_counts, prices)
plt.show()
