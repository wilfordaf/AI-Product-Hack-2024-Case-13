BEGIN;

INSERT INTO categories (title) 
VALUES 
    ('Skills'), 
    ('Specialty'), 
    ('Interests'), 
    ('Country'), 
    ('Age');

INSERT INTO tags (title, category_id)
SELECT unnest(ARRAY[
    'Leadership', 'Management', 'Marketing', 'Strategy', 'Public Speaking', 'Research', 
    'Strategic Planning', 'Data Analysis', 'Accounting', 'Teamwork', 'Leadership Development', 
    'Software Testing', 'UnrealEngine', 'React', 'Angular', 'Django', 'Flask', 'TensorFlow', 
    'PyTorch', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible', 'Selenium', 'CI/CD', 
    'Agile', 'Scrum', 'Git', 'REST', 'MongoDB', 'SQL', 'Figma', 'Sketch', 'AdobeXD', 'Azure', 
    'Hyper-V'
]) AS tag_title, (SELECT id FROM categories WHERE title = 'Skills');

INSERT INTO tags (title, category_id)
SELECT unnest(ARRAY[
    'Backend', 'Frontend', 'Machine Learning Engineer', 'Data Engineer', 'MLOps Engineer', 'Design', 
    'Database Developer', 'System Software Engineer', 'Security Engineer', 'Technical Support Engineer', 
    'Product Manager', 'DevOps', 'NLP', 'Computer Vision', 'Database Administration', 'UX/UI Designer', 
    'Computer Graphics', '3D Modeling', 'Animation', 'Cybersecurity', 'Test Driven Development', 
    'Game Development', 'FinTech', 'IT Consulting', 'System Administrator'
]) AS tag_title, (SELECT id FROM categories WHERE title = 'Specialty');

INSERT INTO tags (title, category_id)
SELECT unnest(ARRAY[
    'Fashion', 'Art', 'Movies', 'Sports', 'Music', 'Business and entrepreneurship', 'Outdoor activities', 
    'Gardening', 'Photography', 'Nature', 'Travel', 'Books', 'Cooking', 'Technology', 'Politics', 
    'Health and wellness', 'Finance and investments', 'Food and dining', 'Beauty', 'Parenting and family', 
    'Education and learning', 'Pets', 'Cars and automobiles', 'Social causes and activism', 'Fitness', 
    'History', 'Science', 'DIY and crafts', 'Gaming'
]) AS tag_title, (SELECT id FROM categories WHERE title = 'Interests');

INSERT INTO tags (title, category_id)
SELECT unnest(ARRAY[
    'India', 'United States', 'Brazil', 'China', 'Russia', 'France', 'United Kingdom', 'Indonesia', 
    'Germany', 'Philippines', 'Japan', 'Italy', 'Nigeria', 'Canada', 'Spain', 'Colombia', 'Thailand', 
    'Mexico', 'Israel', 'Iran', 'Malaysia', 'Guatemala', 'Ethiopia', 'Bulgaria', 'Venezuela', 'Portugal', 
    'Tunisia', 'Syria', 'Sudan', 'Turkey', 'Sri Lanka', 'Uzbekistan', 'South Africa', 'Somalia', 
    'Tanzania', 'Australia', 'Panama', 'Pakistan', 'North Macedonia', 'Netherlands', 'Namibia', 
    'Azerbaijan', 'Lithuania', 'Greece', 'Finland', 'Cuba', 'Croatia', 'Costa Rica', 'Burkina Faso', 
    'Bosnia and Herzegovina', 'Bangladesh', 'Vietnam'
]) AS tag_title, (SELECT id FROM categories WHERE title = 'Country');

INSERT INTO tags (title, category_id)
SELECT unnest(ARRAY['40-49', '20-29', '50-59', '30-39']) AS tag_title, (SELECT id FROM categories WHERE title = 'Age');

COMMIT;