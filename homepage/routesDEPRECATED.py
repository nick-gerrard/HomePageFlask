"""
import os, requests, datetime, lxml, time, json
from flask import Flask, Response, render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
from bs4 import BeautifulSoup
from flask_mail import Message as ExternalMessage
from homepage import app, db, bcrypt,  mail, nyt, openweather
from homepage.forms import (RegistrationForm, LoginForm, LinkForm, DeleteLinkForm, NewNoteForm,
                        ChangeWeatherForm, NewMessageForm, RequestResetForm, ResetPasswordForm)
from homepage.models import User, Note, Link, Message

"""











