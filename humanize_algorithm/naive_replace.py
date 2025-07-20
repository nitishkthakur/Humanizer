import json
import random
import re
import os

# Read the JSON mapping from file using a path relative to this script
json_path = os.path.join(os.path.dirname(__file__), 'naive_humanize_replace_map.json')
with open(json_path, 'r') as f:
    naive_humanize_replace_map = json.load(f)

def naive_humanize_1(replace_map, text, replace_rate=0.8):
    """
    Replaces phrases in the input text according to the replace_map.
    Each phrase is replaced with probability replace_rate.
    Args:
        replace_map (dict): Mapping of phrases to their humanized versions.
        text (str): The input text to humanize.
        replace_rate (float): Probability of replacing a detected phrase (0 to 1).
    Returns:
        tuple: (humanized_text, num_replacements, replacements_dict)
    """

    sorted_keys = sorted(replace_map.keys(), key=len, reverse=True)
    replacements = {}
    total_replacements = 0

    for key in sorted_keys:
        pattern = re.escape(key)
        # Find all matches
        matches = list(re.finditer(pattern, text))
        count = 0
        # Replace with probability
        def repl(m):
            nonlocal count
            if random.random() < replace_rate:
                count += 1
                return replace_map[key]
            else:
                return m.group(0)
        text = re.sub(pattern, repl, text)
        if count > 0:
            replacements[key] = count
            total_replacements += count
    return text, total_replacements, replacements


result_text, num_replacements, replacements = naive_humanize_1(
    naive_humanize_replace_map,
    """The Importance of Gender Sensitization: Breaking Down Barriers and Building a More Inclusive Society

In today's world, gender equality is a fundamental human right that is still not fully realized. Despite progress in many areas, women and marginalized gender groups continue to face significant barriers and biases that prevent them from achieving their full potential. This is where gender sensitization comes in – a crucial process that aims to raise awareness and challenge societal norms, attitudes, and behaviors that perpetuate gender-based discrimination.

What is Gender Sensitization?

Gender sensitization refers to the process of educating individuals about the social and cultural constructs of gender, and how these constructs can lead to inequality and discrimination. It involves recognizing and challenging the unconscious biases and stereotypes that are deeply ingrained in our society, and promoting a culture of respect, empathy, and inclusivity. Gender sensitization is not just about women's empowerment, but also about creating a more equitable and just society for all individuals, regardless of their gender identity or expression.

Why is Gender Sensitization Important?

Gender sensitization is essential for several reasons. Firstly, it helps to break down the patriarchal norms and stereotypes that have been perpetuated for centuries, and which continue to hold women and marginalized gender groups back. By challenging these norms, we can create a more level playing field, where everyone has an equal opportunity to succeed and thrive. Secondly, gender sensitization helps to prevent gender-based violence and harassment, which are pervasive problems that affect millions of people around the world. By promoting a culture of respect and empathy, we can reduce the incidence of these crimes and create a safer and more supportive environment for all.

How Can We Achieve Gender Sensitization?

Achieving gender sensitization requires a multi-faceted approach that involves individuals, communities, organizations, and governments. Here are some strategies that can help:

    Education and Awareness: Educating individuals about gender issues and challenging stereotypes is a critical step in promoting gender sensitization. This can be done through workshops, training programs, and awareness campaigns.
    Policy Reforms: Governments and organizations can implement policies that promote gender equality, such as equal pay, parental leave, and anti-discrimination laws.
    Community Engagement: Engaging with local communities and promoting dialogue and discussion about gender issues can help to raise awareness and challenge norms.
    Role Modeling: Leaders and influencers can play a critical role in promoting gender sensitization by modeling respectful and inclusive behavior.

Challenges and Opportunities

Despite the importance of gender sensitization, there are several challenges that need to be addressed. These include:

    Resistance to Change: Some individuals and groups may resist changes to traditional gender roles and norms, which can make it difficult to promote gender sensitization.
    Lack of Resources: Limited resources and funding can hinder efforts to promote gender sensitization, particularly in low-income communities.
    Cultural and Social Barriers: Cultural and social barriers, such as patriarchal norms and stereotypes, can make it difficult to promote gender sensitization.

However, there are also many opportunities for promoting gender sensitization. These include:

    Growing Awareness: There is growing awareness and recognition of the importance of gender equality, which can help to drive efforts to promote gender sensitization.
    Technological Advances: Technology can be a powerful tool for promoting gender sensitization, particularly through social media and online campaigns.
    Global Cooperation: International cooperation and collaboration can help to promote gender sensitization and share best practices.

Conclusion

In conclusion, gender sensitization is a critical process that is essential for promoting gender equality and challenging societal norms and attitudes that perpetuate discrimination. By educating individuals, promoting policy reforms, engaging with communities, and modeling respectful behavior, we can create a more inclusive and equitable society for all. While there are challenges to be addressed, there are also many opportunities for promoting gender sensitization and driving positive change. Ultimately, gender sensitization is a journey that requires commitment, dedication, and collective effort, but the rewards are well worth it – a more just, equitable, and peaceful world for all.

"""
)

print(result_text)
print(f"\nTotal replacements: {num_replacements}")
print("Replacements made:")
for k, v in replacements.items():
    print(f"'{k}' -> {v} time(s)")