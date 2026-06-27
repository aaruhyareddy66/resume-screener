import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load real dataset
df = pd.read_csv('ResumeData.csv')
df = df[['Category', 'Resume_str']].dropna()
df.columns = ['category', 'resume_text']

# Map categories
category_map = {
    'INFORMATION-TECHNOLOGY': 'Full Stack Developer',
    'ENGINEERING': 'Full Stack Developer',
    'DESIGNER': 'Full Stack Developer',
    'DIGITAL-MEDIA': 'Full Stack Developer',
    'CONSULTANT': 'Business Analyst',
    'BUSINESS-DEVELOPMENT': 'Business Analyst',
    'FINANCE': 'Business Analyst',
    'BANKING': 'Business Analyst',
    'HR': 'Business Analyst',
    'SALES': 'Business Analyst',
    'HEALTHCARE': 'Others',
    'TEACHER': 'Others',
    'ADVOCATE': 'Others',
    'ACCOUNTANT': 'Others',
    'PUBLIC-RELATIONS': 'Others',
    'AGRICULTURE': 'Others',
    'AUTOMOBILE': 'Others',
    'BPO': 'Others',
    'ARTS': 'Others',
    'APPAREL': 'Others',
    'CONSTRUCTION': 'Others',
    'AVIATION': 'Others',
    'CHEF': 'Others',
    'FITNESS': 'Others',
}

df['category'] = df['category'].map(category_map)
df = df.dropna()

# Add custom Java Developer resumes
java_resumes = [
    "Java developer Spring Boot REST API MySQL Hibernate Maven Git microservices Docker AWS",
    "Senior Java engineer Spring framework Hibernate JPA MySQL PostgreSQL Maven Gradle Jenkins",
    "Java backend developer Spring Boot Spring MVC REST API SQL Oracle Git Jenkins CI/CD",
    "Java developer J2EE Spring Hibernate Struts MySQL Oracle WebLogic JBoss application server",
    "Java programmer Spring Boot Microservices Docker Kubernetes AWS REST API development",
    "Java developer Android mobile application kotlin java firebase google play store",
    "Full stack Java developer Spring Boot React MySQL Docker AWS deployment production",
    "Java engineer Spring Boot Spring Security JWT REST API MySQL Redis cache session",
    "Java software engineer multithreading collections framework design patterns SOLID principles",
    "Java developer Spring MVC Hibernate JPA RESTful web services XML JSON parsing",
    "Backend Java developer Spring Boot microservices architecture Docker container deployment",
    "Java programmer Core Java JDBC Servlet JSP Spring MVC Hibernate MySQL project",
    "Java developer Spring Boot unit testing JUnit Mockito TDD test driven development",
    "Senior Java engineer distributed systems Apache Kafka messaging queue Spring Boot",
    "Java developer Spring Boot Angular full stack MySQL Docker Kubernetes AWS cloud",
    "Java software developer Spring framework OOP design patterns Maven build tool Git",
    "Java backend engineer Spring Boot REST API PostgreSQL Redis Elasticsearch Docker",
    "Java developer Spring Security OAuth2 JWT token authentication authorization Spring Boot",
    "Java programmer Spring Boot batch processing scheduled tasks MySQL database performance",
    "Java developer Spring Cloud microservices Eureka service discovery Ribbon load balancer",
] * 3

# Add custom DevOps resumes
devops_resumes = [
    "DevOps engineer AWS Docker Kubernetes Jenkins CI/CD Linux bash scripting automation",
    "Cloud engineer AWS Azure GCP Terraform Ansible Docker Kubernetes infrastructure DevOps",
    "DevOps AWS EC2 S3 RDS Lambda CloudFormation Docker Jenkins Git pipeline deployment",
    "Site reliability engineer SRE Kubernetes Docker Prometheus Grafana Linux monitoring",
    "DevOps engineer CI/CD Jenkins GitLab Docker Kubernetes AWS Azure cloud deployment",
    "Cloud DevOps AWS Terraform Docker Kubernetes Ansible Python bash automation scripting",
    "Infrastructure engineer AWS Docker Kubernetes Terraform Ansible monitoring alerting",
    "DevOps engineer Linux shell scripting Python Docker Jenkins AWS deployment pipeline",
    "Cloud architect AWS GCP Azure microservices Docker Kubernetes serverless Lambda",
    "DevOps engineer Ansible Chef Puppet configuration management Docker containerization",
    "Platform engineer Kubernetes Helm charts Docker AWS EKS ECS container orchestration",
    "DevOps specialist Jenkins pipeline GitLab CI GitHub Actions automated testing deployment",
    "Cloud DevOps engineer AWS CloudWatch monitoring logging ELK stack Kibana Elasticsearch",
    "DevOps engineer Nginx Apache load balancer SSL certificate Linux server administration",
    "Site reliability SRE Google Cloud GKE Kubernetes Docker monitoring observability",
    "DevOps automation engineer Python bash scripting AWS Lambda serverless functions",
    "DevOps engineer HashiCorp Vault secrets management Terraform infrastructure as code",
    "Cloud operations engineer AWS Cost optimization auto scaling load balancing high availability",
    "DevOps engineer Prometheus Grafana alerting metrics monitoring Kubernetes cluster",
    "Infrastructure DevOps AWS networking VPC subnets security groups route tables DNS",
] * 3

# Add custom Data Scientist resumes
ds_resumes = [
    "Data scientist machine learning deep learning tensorflow keras python pandas numpy scikit",
    "Machine learning engineer scikit-learn tensorflow pytorch model deployment MLOps python",
    "Data scientist NLP natural language processing BERT transformers huggingface python",
    "Data analyst SQL python tableau power bi excel statistics data visualization matplotlib",
    "ML engineer deep learning CNN RNN LSTM computer vision image classification python",
    "Data scientist predictive modeling regression classification clustering python R statistics",
    "AI researcher deep learning generative models GAN transformer architecture pytorch",
    "Data scientist feature engineering model selection hyperparameter tuning cross validation",
    "Machine learning python scikit-learn XGBoost LightGBM gradient boosting ensemble methods",
    "Data scientist time series forecasting ARIMA LSTM prophet python pandas statistics",
    "NLP engineer BERT GPT transformer fine tuning text classification sentiment analysis",
    "Computer vision engineer OpenCV CNN object detection YOLO image segmentation pytorch",
    "Data scientist A/B testing hypothesis testing statistical analysis python scipy numpy",
    "ML ops engineer model deployment docker kubernetes flask fastapi REST API python",
    "Data scientist recommendation system collaborative filtering matrix factorization python",
    "Deep learning researcher neural network architecture optimization GPU training pytorch",
    "Data analyst Python SQL Tableau dashboard KPI metrics business intelligence reporting",
    "Machine learning engineer feature store model registry MLflow experiment tracking",
    "Data scientist reinforcement learning Q-learning policy gradient OpenAI gym python",
    "NLP data scientist text mining information extraction named entity recognition spacy",
] * 3

# Create additional dataframes
java_df = pd.DataFrame({
    'category': ['Java Developer'] * len(java_resumes),
    'resume_text': java_resumes
})

devops_df = pd.DataFrame({
    'category': ['DevOps Engineer'] * len(devops_resumes),
    'resume_text': devops_resumes
})

ds_df = pd.DataFrame({
    'category': ['Data Scientist'] * len(ds_resumes),
    'resume_text': ds_resumes
})

# Combine all data
df = pd.concat([df, java_df, devops_df, ds_df], ignore_index=True)

print(f"Total dataset: {len(df)} resumes")
print(f"Categories:\n{df['category'].value_counts()}")

# TF-IDF
tfidf = TfidfVectorizer(max_features=3000, stop_words='english', ngram_range=(1,2))
X = tfidf.fit_transform(df['resume_text'])
y = df['category']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
print(classification_report(y_test, y_pred))

# Save
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

print("\nModel saved!")