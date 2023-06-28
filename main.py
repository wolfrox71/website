from flask import Flask, Blueprint, url_for, render_template, redirect

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)