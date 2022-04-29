from django.forms import ModelForm, Textarea
from .models import Bid, Comment, User, Auction

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 20, 'rows': 5, 'placeholder': 'Post a comment for this auction'}),
        }

class CloseForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['is_open']

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'starting_bid', 'description', 'category', 'image']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': 'Enter your bid amount'
        }
