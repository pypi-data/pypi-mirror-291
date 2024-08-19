from setuptools import setup,find_packages
with open('README.md',encoding='utf-8') as f:
    long_des = f.read()


setup(name='AI-ChatGPT-Free',
      version='0.0.1',
      author='龙亮哲',
      author_email='17818883308@139.com',
      description='免费的ChatGPT Python库',
      long_description=long_des,
      long_description_content_type="text/markdown",
      url='https://github.com/longliangzhe/ChatGpt-free',
      packages=find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      platforms=['Windows','Linux'],
      python_requires='>=3',
)