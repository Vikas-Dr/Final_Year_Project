"""
Role-based question bank for the AI Interview Evaluation System.
Contains MCQ, theory, and coding questions for common job roles.
"""
from typing import Dict, List

# ─── Question Types ───────────────────────────────────────────────────────────
# MCQ: question, options (list of 4), correct_index (0-3)
# Theory: question, expected_keywords (list)
# Coding: question, function_name, test_cases [{input, expected_output}]

QUESTION_BANK: Dict[str, Dict[str, List]] = {

    # ──────────────────────────── Python Engineer ────────────────────────────
    "Python Engineer": {
        "mcq": [
            {
                "question": "Which keyword is used to define a generator function in Python?",
                "options": ["return", "yield", "async", "lambda"],
                "correct_index": 1,
            },
            {
                "question": "What does the GIL stand for in Python?",
                "options": ["Global Import Lock", "Global Interpreter Lock", "General Iteration Loop", "Group Interface Layer"],
                "correct_index": 1,
            },
            {
                "question": "Which of the following is an immutable data type in Python?",
                "options": ["list", "dict", "tuple", "set"],
                "correct_index": 2,
            },
            {
                "question": "What is the output of `print(type([]) == list)`?",
                "options": ["False", "True", "Error", "None"],
                "correct_index": 1,
            },
            {
                "question": "Which module is used for regular expressions in Python?",
                "options": ["regex", "re", "pattern", "match"],
                "correct_index": 1,
            },
            {
                "question": "What does `*args` in a function definition do?",
                "options": ["Accepts keyword arguments", "Accepts a fixed number of arguments", "Accepts variable positional arguments", "Returns multiple values"],
                "correct_index": 2,
            },
            {
                "question": "Which built-in function returns the length of an object?",
                "options": ["size()", "count()", "len()", "length()"],
                "correct_index": 2,
            },
            {
                "question": "What is the correct way to open a file for writing in Python?",
                "options": ["open(file, 'r')", "open(file, 'w')", "open(file, 'a')", "open(file, 'rb')"],
                "correct_index": 1,
            },
            {
                "question": "Which statement is used to handle exceptions in Python?",
                "options": ["catch", "try-except", "handle", "error"],
                "correct_index": 1,
            },
            {
                "question": "What is a list comprehension in Python?",
                "options": [
                    "A way to import libraries",
                    "A concise way to create lists using a single line expression",
                    "A method to sort lists",
                    "A way to declare global variables",
                ],
                "correct_index": 1,
            },
        ],
        "theory": [
            {
                "question": "Explain the difference between a list and a tuple in Python.",
                "expected_keywords": ["mutable", "immutable", "list", "tuple", "modify", "ordered", "hashable"],
            },
            {
                "question": "What is object-oriented programming? Explain with Python examples.",
                "expected_keywords": ["class", "object", "inheritance", "encapsulation", "polymorphism", "method", "instance"],
            },
            {
                "question": "Explain how Python's garbage collection works.",
                "expected_keywords": ["reference counting", "garbage collector", "memory", "cyclic", "gc module", "unreachable"],
            },
            {
                "question": "What are decorators in Python and how do they work?",
                "expected_keywords": ["decorator", "wrapper", "function", "@ symbol", "higher-order", "modify behaviour"],
            },
            {
                "question": "What is the difference between `==` and `is` in Python?",
                "expected_keywords": ["equality", "identity", "value", "reference", "object", "memory address"],
            },
        ],
        "coding": [
            {
                "question": "Write a Python function `reverse_string(s)` that takes a string `s` and returns it reversed.",
                "function_name": "reverse_string",
                "test_cases": [
                    {"input": ["hello"], "expected": "olleh"},
                    {"input": ["python"], "expected": "nohtyp"},
                    {"input": [""], "expected": ""},
                    {"input": ["a"], "expected": "a"},
                ],
            },
            {
                "question": "Write a Python function `is_palindrome(s)` that returns True if the string is a palindrome, False otherwise.",
                "function_name": "is_palindrome",
                "test_cases": [
                    {"input": ["racecar"], "expected": True},
                    {"input": ["hello"], "expected": False},
                    {"input": ["madam"], "expected": True},
                    {"input": ["a"], "expected": True},
                ],
            },
            {
                "question": "Write a Python function `factorial(n)` that returns the factorial of a non-negative integer `n`.",
                "function_name": "factorial",
                "test_cases": [
                    {"input": [0], "expected": 1},
                    {"input": [1], "expected": 1},
                    {"input": [5], "expected": 120},
                    {"input": [7], "expected": 5040},
                ],
            },
        ],
    },

    # ──────────────────────────── AI Engineer ────────────────────────────────
    "AI Engineer": {
        "mcq": [
            {
                "question": "What does NLP stand for?",
                "options": ["Natural Language Processing", "Neural Learning Protocol", "Network Layer Protocol", "Numeric Language Parsing"],
                "correct_index": 0,
            },
            {
                "question": "Which algorithm is commonly used for text classification?",
                "options": ["K-Means", "Naive Bayes", "PCA", "DBSCAN"],
                "correct_index": 1,
            },
            {
                "question": "What is overfitting in machine learning?",
                "options": [
                    "Model performs poorly on training data",
                    "Model performs well on training data but poorly on test data",
                    "Model is too simple",
                    "Model has too few parameters",
                ],
                "correct_index": 1,
            },
            {
                "question": "Which activation function is commonly used in hidden layers of deep neural networks?",
                "options": ["Sigmoid", "Softmax", "ReLU", "Linear"],
                "correct_index": 2,
            },
            {
                "question": "What does TF-IDF stand for?",
                "options": ["Training-Feature Inverse Document Frequency", "Term Frequency-Inverse Document Frequency", "Total Frequency Inner Document Function", "Text Filter Inverse Document Format"],
                "correct_index": 1,
            },
            {
                "question": "Which library provides pre-trained word embeddings like Word2Vec?",
                "options": ["NumPy", "Pandas", "Gensim", "Matplotlib"],
                "correct_index": 2,
            },
            {
                "question": "What is a confusion matrix used for?",
                "options": ["Data preprocessing", "Evaluating classification model performance", "Feature extraction", "Training neural networks"],
                "correct_index": 1,
            },
            {
                "question": "In supervised learning, what is the training data composed of?",
                "options": ["Only inputs", "Only outputs", "Inputs and corresponding correct outputs", "Random data"],
                "correct_index": 2,
            },
            {
                "question": "Which technique helps prevent overfitting in neural networks?",
                "options": ["More training data only", "Dropout", "Increasing learning rate", "Removing validation set"],
                "correct_index": 1,
            },
            {
                "question": "What is the purpose of the softmax function in neural networks?",
                "options": ["Normalize hidden layer outputs", "Convert outputs to binary", "Convert outputs to probabilities summing to 1", "Apply regularization"],
                "correct_index": 2,
            },
        ],
        "theory": [
            {
                "question": "Explain the concept of semantic similarity in NLP.",
                "expected_keywords": ["meaning", "context", "cosine similarity", "embeddings", "word vectors", "sentence", "similarity score"],
            },
            {
                "question": "What is the difference between supervised and unsupervised learning?",
                "expected_keywords": ["labeled", "unlabeled", "training data", "classification", "clustering", "supervised", "unsupervised"],
            },
            {
                "question": "Explain what a transformer model is and its key components.",
                "expected_keywords": ["attention", "self-attention", "encoder", "decoder", "BERT", "GPT", "positional encoding"],
            },
            {
                "question": "What is resume parsing and how can NLP be applied to it?",
                "expected_keywords": ["extract", "text", "entities", "skills", "education", "NER", "regular expressions", "sections"],
            },
            {
                "question": "What evaluation metrics would you use for an interview scoring system?",
                "expected_keywords": ["accuracy", "precision", "recall", "F1", "keyword matching", "cosine similarity", "scoring rubric"],
            },
        ],
        "coding": [
            {
                "question": "Write a Python function `word_count(text)` that takes a string and returns a dictionary with each word as a key and its frequency as the value. Words should be lowercase.",
                "function_name": "word_count",
                "test_cases": [
                    {"input": ["hello world hello"], "expected": {"hello": 2, "world": 1}},
                    {"input": ["the cat sat on the mat"], "expected": {"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1}},
                    {"input": [""], "expected": {}},
                ],
            },
            {
                "question": "Write a Python function `cosine_similarity(vec1, vec2)` that computes the cosine similarity between two lists of numbers.",
                "function_name": "cosine_similarity",
                "test_cases": [
                    {"input": [[1, 0], [1, 0]], "expected": 1.0},
                    {"input": [[1, 0], [0, 1]], "expected": 0.0},
                ],
            },
            {
                "question": "Write a Python function `remove_stopwords(text, stopwords)` that removes all words in the stopwords list from the text string and returns the cleaned text.",
                "function_name": "remove_stopwords",
                "test_cases": [
                    {"input": ["the quick brown fox", ["the", "a", "an"]], "expected": "quick brown fox"},
                    {"input": ["I am a student", ["I", "am", "a"]], "expected": "student"},
                ],
            },
        ],
    },

    # ──────────────────────────── Web Developer ───────────────────────────────
    "Web Developer": {
        "mcq": [
            {
                "question": "What does HTML stand for?",
                "options": ["HyperText Markup Language", "HighText Machine Language", "HyperText Multi Language", "High Transfer Markup Language"],
                "correct_index": 0,
            },
            {
                "question": "Which CSS property is used to change text colour?",
                "options": ["text-color", "font-color", "color", "foreground"],
                "correct_index": 2,
            },
            {
                "question": "What is the correct syntax for a JavaScript arrow function?",
                "options": ["function => {}", "const fn = () => {}", "fn = function() =>", "arrow fn() {}"],
                "correct_index": 1,
            },
            {
                "question": "Which HTTP method is used to retrieve data from a server?",
                "options": ["POST", "PUT", "DELETE", "GET"],
                "correct_index": 3,
            },
            {
                "question": "What does REST stand for?",
                "options": ["Remote Execution State Transfer", "Representational State Transfer", "Reactive Event Stream Technology", "Relational State Transfer"],
                "correct_index": 1,
            },
            {
                "question": "In React, what hook is used to manage component state?",
                "options": ["useEffect", "useRef", "useState", "useContext"],
                "correct_index": 2,
            },
            {
                "question": "Which CSS layout system allows items to be arranged in rows and columns?",
                "options": ["Flexbox", "Grid", "Float", "Position"],
                "correct_index": 1,
            },
            {
                "question": "What is the purpose of a JWT token?",
                "options": ["Store passwords securely", "Transfer files", "Authenticate and authorize API requests", "Compress data"],
                "correct_index": 2,
            },
            {
                "question": "Which tag is used to link a CSS file in HTML?",
                "options": ["<style>", "<css>", "<link>", "<script>"],
                "correct_index": 2,
            },
            {
                "question": "What is CORS?",
                "options": [
                    "A method to compress responses",
                    "Cross-Origin Resource Sharing — controls browser resource access between origins",
                    "A CSS framework",
                    "A JavaScript testing tool",
                ],
                "correct_index": 1,
            },
        ],
        "theory": [
            {
                "question": "Explain the difference between `localStorage` and `sessionStorage` in JavaScript.",
                "expected_keywords": ["localStorage", "sessionStorage", "persistent", "session", "browser", "data", "key-value", "expiry"],
            },
            {
                "question": "What is the virtual DOM in React and why is it important?",
                "expected_keywords": ["virtual DOM", "real DOM", "diffing", "reconciliation", "performance", "re-render", "React"],
            },
            {
                "question": "Explain the concept of RESTful API design.",
                "expected_keywords": ["stateless", "HTTP methods", "GET", "POST", "PUT", "DELETE", "endpoints", "resources", "JSON"],
            },
            {
                "question": "What is the box model in CSS?",
                "expected_keywords": ["margin", "padding", "border", "content", "box-sizing", "width", "height"],
            },
            {
                "question": "Explain the difference between synchronous and asynchronous JavaScript.",
                "expected_keywords": ["synchronous", "asynchronous", "callback", "promise", "async", "await", "event loop", "non-blocking"],
            },
        ],
        "coding": [
            {
                "question": "Write a Python function `sum_list(numbers)` that takes a list of numbers and returns their sum.",
                "function_name": "sum_list",
                "test_cases": [
                    {"input": [[1, 2, 3, 4, 5]], "expected": 15},
                    {"input": [[]], "expected": 0},
                    {"input": [[-1, 1]], "expected": 0},
                    {"input": [[10, 20]], "expected": 30},
                ],
            },
            {
                "question": "Write a Python function `flatten(nested_list)` that takes a list of lists and returns a single flat list.",
                "function_name": "flatten",
                "test_cases": [
                    {"input": [[[1, 2], [3, 4]]], "expected": [1, 2, 3, 4]},
                    {"input": [[[1], [2], [3]]], "expected": [1, 2, 3]},
                    {"input": [[[]]], "expected": []},
                ],
            },
            {
                "question": "Write a Python function `is_even(n)` that returns True if n is even, False otherwise.",
                "function_name": "is_even",
                "test_cases": [
                    {"input": [2], "expected": True},
                    {"input": [3], "expected": False},
                    {"input": [0], "expected": True},
                    {"input": [7], "expected": False},
                ],
            },
        ],
    },

    # ──────────────────────────── Data Scientist ─────────────────────────────
    "Data Scientist": {
        "mcq": [
            {
                "question": "What does EDA stand for?",
                "options": ["Extended Data Analysis", "Exploratory Data Analysis", "External Data Aggregation", "Experimental Data Architecture"],
                "correct_index": 1,
            },
            {
                "question": "Which library is primarily used for numerical computing in Python?",
                "options": ["Pandas", "Matplotlib", "NumPy", "Seaborn"],
                "correct_index": 2,
            },
            {
                "question": "What is the purpose of normalization in machine learning?",
                "options": ["Remove duplicate data", "Scale features to a similar range", "Increase training speed by reducing epochs", "Convert categorical data to numerical"],
                "correct_index": 1,
            },
            {
                "question": "Which algorithm is used for dimensionality reduction?",
                "options": ["K-Means", "PCA", "Random Forest", "SVM"],
                "correct_index": 1,
            },
            {
                "question": "What is a p-value in statistics?",
                "options": [
                    "The probability that the model is correct",
                    "The probability of observing results at least as extreme as those measured, assuming the null hypothesis is true",
                    "The percentage of variance explained by a model",
                    "The correlation coefficient between two variables",
                ],
                "correct_index": 1,
            },
            {
                "question": "Which pandas method is used to read a CSV file?",
                "options": ["pd.load_csv()", "pd.read_csv()", "pd.open_csv()", "pd.import_csv()"],
                "correct_index": 1,
            },
            {
                "question": "What is the purpose of a train-test split?",
                "options": ["Reduce dataset size", "Evaluate model performance on unseen data", "Increase model accuracy", "Remove outliers"],
                "correct_index": 1,
            },
            {
                "question": "Which of the following is a supervised learning algorithm?",
                "options": ["K-Means clustering", "DBSCAN", "Linear Regression", "PCA"],
                "correct_index": 2,
            },
            {
                "question": "What does RMSE measure?",
                "options": ["Classification accuracy", "Root Mean Squared Error between predictions and actuals", "Recall in classification", "Range of feature values"],
                "correct_index": 1,
            },
            {
                "question": "Which type of plot is best for showing the distribution of a single variable?",
                "options": ["Scatter plot", "Bar chart", "Histogram", "Line chart"],
                "correct_index": 2,
            },
        ],
        "theory": [
            {
                "question": "What is the bias-variance tradeoff in machine learning?",
                "expected_keywords": ["bias", "variance", "overfitting", "underfitting", "tradeoff", "model complexity", "error"],
            },
            {
                "question": "Explain what cross-validation is and why it is used.",
                "expected_keywords": ["cross-validation", "k-fold", "training", "validation", "generalisation", "overfitting", "average"],
            },
            {
                "question": "What is feature engineering and why is it important?",
                "expected_keywords": ["features", "transform", "create", "improve", "model performance", "domain knowledge", "encoding"],
            },
            {
                "question": "Explain the difference between correlation and causation.",
                "expected_keywords": ["correlation", "causation", "relationship", "cause", "effect", "confounding", "association"],
            },
            {
                "question": "What is a Random Forest and how does it work?",
                "expected_keywords": ["ensemble", "decision trees", "bagging", "bootstrap", "random features", "majority voting", "classification"],
            },
        ],
        "coding": [
            {
                "question": "Write a Python function `mean(numbers)` that computes the arithmetic mean of a list of numbers.",
                "function_name": "mean",
                "test_cases": [
                    {"input": [[1, 2, 3, 4, 5]], "expected": 3.0},
                    {"input": [[10, 20]], "expected": 15.0},
                    {"input": [[7]], "expected": 7.0},
                ],
            },
            {
                "question": "Write a Python function `find_max(numbers)` that returns the maximum value in a list without using the built-in max() function.",
                "function_name": "find_max",
                "test_cases": [
                    {"input": [[3, 1, 4, 1, 5, 9]], "expected": 9},
                    {"input": [[-1, -5, -3]], "expected": -1},
                    {"input": [[42]], "expected": 42},
                ],
            },
            {
                "question": "Write a Python function `count_above_threshold(numbers, threshold)` that returns the count of numbers in the list that are strictly above the threshold.",
                "function_name": "count_above_threshold",
                "test_cases": [
                    {"input": [[1, 5, 3, 8, 2], 4], "expected": 2},
                    {"input": [[1, 2, 3], 5], "expected": 0},
                    {"input": [[10, 20, 30], 0], "expected": 3},
                ],
            },
        ],
    },

    # ──────────────────────────── Full Stack Developer ────────────────────────
    "Full Stack Developer": {
        "mcq": [
            {
                "question": "What is the difference between SQL and NoSQL databases?",
                "options": [
                    "SQL is faster than NoSQL",
                    "SQL uses structured tables; NoSQL uses flexible document/key-value stores",
                    "NoSQL supports joins; SQL does not",
                    "SQL databases cannot scale horizontally",
                ],
                "correct_index": 1,
            },
            {
                "question": "Which HTTP status code indicates a successful request?",
                "options": ["404", "500", "200", "301"],
                "correct_index": 2,
            },
            {
                "question": "What is middleware in Express.js?",
                "options": [
                    "A database layer",
                    "A function that has access to the request and response objects in the request-response cycle",
                    "A front-end component",
                    "A build tool",
                ],
                "correct_index": 1,
            },
            {
                "question": "What is Docker used for?",
                "options": ["Version control", "Containerising applications for consistent environments", "Frontend UI design", "Database management"],
                "correct_index": 1,
            },
            {
                "question": "Which command initializes a new Git repository?",
                "options": ["git start", "git init", "git create", "git new"],
                "correct_index": 1,
            },
            {
                "question": "What does API stand for?",
                "options": ["Application Programming Interface", "Automated Process Integration", "Application Process Interaction", "Automated Programming Interface"],
                "correct_index": 0,
            },
            {
                "question": "In React, what is the purpose of `useEffect`?",
                "options": [
                    "To manage component state",
                    "To perform side effects such as API calls or subscriptions",
                    "To create context",
                    "To memoize values",
                ],
                "correct_index": 1,
            },
            {
                "question": "Which of the following is NOT a JavaScript framework?",
                "options": ["Vue.js", "Angular", "Django", "React"],
                "correct_index": 2,
            },
            {
                "question": "What does CI/CD stand for?",
                "options": ["Code Integration / Code Deployment", "Continuous Integration / Continuous Delivery", "Cloud Infrastructure / Cloud Deployment", "Component Integration / Component Delivery"],
                "correct_index": 1,
            },
            {
                "question": "Which SQL clause filters rows based on a condition?",
                "options": ["GROUP BY", "ORDER BY", "WHERE", "HAVING"],
                "correct_index": 2,
            },
        ],
        "theory": [
            {
                "question": "Explain the MVC design pattern and how it applies to web development.",
                "expected_keywords": ["model", "view", "controller", "separation", "concerns", "data", "presentation", "logic"],
            },
            {
                "question": "What are the key differences between authentication and authorisation?",
                "expected_keywords": ["authentication", "authorisation", "identity", "verify", "permissions", "access", "roles", "JWT"],
            },
            {
                "question": "Explain what an ORM is and give an example.",
                "expected_keywords": ["ORM", "object relational mapping", "SQLAlchemy", "database", "query", "model", "table"],
            },
            {
                "question": "What is the purpose of indexing in a database?",
                "expected_keywords": ["index", "performance", "query speed", "search", "B-tree", "lookup", "slower writes"],
            },
            {
                "question": "How would you optimise a slow REST API endpoint?",
                "expected_keywords": ["caching", "database index", "pagination", "query optimisation", "async", "load balancer", "profiling"],
            },
        ],
        "coding": [
            {
                "question": "Write a Python function `fibonacci(n)` that returns the nth Fibonacci number (0-indexed, so fibonacci(0)=0, fibonacci(1)=1, fibonacci(2)=1).",
                "function_name": "fibonacci",
                "test_cases": [
                    {"input": [0], "expected": 0},
                    {"input": [1], "expected": 1},
                    {"input": [6], "expected": 8},
                    {"input": [10], "expected": 55},
                ],
            },
            {
                "question": "Write a Python function `is_prime(n)` that returns True if n is a prime number, False otherwise.",
                "function_name": "is_prime",
                "test_cases": [
                    {"input": [2], "expected": True},
                    {"input": [4], "expected": False},
                    {"input": [17], "expected": True},
                    {"input": [1], "expected": False},
                ],
            },
            {
                "question": "Write a Python function `count_unique(lst)` that returns the number of unique elements in a list.",
                "function_name": "count_unique",
                "test_cases": [
                    {"input": [[1, 2, 2, 3, 3, 3]], "expected": 3},
                    {"input": [[1, 1, 1]], "expected": 1},
                    {"input": [[]], "expected": 0},
                    {"input": [[4, 5, 6]], "expected": 3},
                ],
            },
        ],
    },
}

# Roles available in the system
AVAILABLE_ROLES = list(QUESTION_BANK.keys())

# Default fallback role
DEFAULT_ROLE = "Python Engineer"


def get_questions_for_role(role: str) -> Dict[str, List]:
    """Return the question set for a given role, falling back to Python Engineer."""
    return QUESTION_BANK.get(role, QUESTION_BANK[DEFAULT_ROLE])
