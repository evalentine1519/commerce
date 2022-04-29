from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from .models import User, Auction, Bid, Comment, Category
from .forms import CommentForm, CloseForm, AuctionForm, BidForm


def index(request):
    auction_list = Auction.objects.all()
    bid_list = Bid.objects.all()
    bid_table = {}
    for auction in auction_list:
        bid_table[auction.title] = Bid.objects.get(item=auction).amount

    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        'heading': 'Active Listings',
        "bid_table": bid_table
    })

def category(request, category_id):
    if category_id:
        auction_list = Auction.objects.all()
        bid_list = Bid.objects.all()
        bid_table = {}
        for auction in auction_list:
            bid_table[auction.title] = Bid.objects.get(item=auction).amount

        return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(category=category_id),
        'heading': 'Auctions in category: ',
        'catname': Category.objects.get(pk=category_id),
        "bid_table": bid_table
    })
    else:
        return render(request, "auctions/category.html", {
            "categories": Category.objects.all()
        })

@login_required
def watchlist(request):
    #If request.method is 'POST', then we're adding to our watchlist.
    #Get auction_id from request.POST.get('auction_id'), add to user's watchlist as a comma-separated integer for later reference
    user = User.objects.get(username=request.user)

    auction_list = Auction.objects.all()
    bid_list = Bid.objects.all()
    bid_table = {}
    for auction in auction_list:
        bid_table[auction.title] = Bid.objects.get(item=auction).amount

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            if user.watchlist == None:
                user.watchlist = request.POST.get('auction_id')
            else:
                user.watchlist = user.watchlist + "," + request.POST.get('auction_id')
            user.save(update_fields=['watchlist'])
        else:
            watchlist = User.objects.get(username=request.user).watchlist
            watchlist = watchlist.split(',')
            watchlist.remove(str(request.POST.get('auction_id')))
            watchlist = ",".join(watchlist)
            user.watchlist = watchlist
            user.save(update_fields=['watchlist'])
    #    return render(request, "auctions/index.html")
    #else:
    #    return render(request, "auctions/index.html")

    auction_list = []
    auction_item = []
    print(len(user.watchlist))
    for i in range(len(user.watchlist)):
        #if (int(i)%2 == 0):
        #    auction_list.append(int(i))

        if i == (len(user.watchlist)-1):
            print('last item on the list')
            auction_item.append(user.watchlist[i])
            auction_item = ''.join(auction_item)
            print('appending ' + auction_item + 'to auction_list')
            auction_list.append(int(auction_item))
        elif user.watchlist[i].isdigit():
            auction_item.append(user.watchlist[i])
            print("appending " + user.watchlist[i])
            print('index is ' + str(i))
        else:
            print('hit a comma')
            auction_item = ''.join(auction_item)
            print('appending ' + auction_item + 'to auction_list')
            auction_list.append(int(auction_item))
            auction_item = []
        #try:
        #    auction_item.append(str(int(i)))
        #    print('appended' + str(int(i)))
        #except:
        #    print('hit a comma')
        #    auction_item = ''.join(auction_item)
        #    print('appending ' + auction_item + 'to auction_list')
        #    auction_list.append(int(auction_item))
        #    pass
    print(auction_list)
    print('user.watchlist: ' + user.watchlist)
    print(Auction.objects.filter(pk__in=auction_list))
    return render(request, "auctions/index.html", {
            'auctions': Auction.objects.filter(pk__in=auction_list),
            "heading": 'Auctions in your watch list',
            "bid_table": bid_table
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def auction(request, auction_id):
    message=""
    #username = request.user
    auction = get_object_or_404(Auction, pk=auction_id)
    is_owner = False
    bid = Bid.objects.get(item=auction)
    bidamount = bid.amount
    #auction_owner = auction.owner
    #print(username)
    #print(auction_owner)

    #dump user's watchlist into a list, check if this auction is already on the list
    watchlist = User.objects.get(username=request.user).watchlist
    watchlist = watchlist.split(',')
    try:
        if watchlist.index(str(auction_id)):
            on_watchlist = True
            print('On watchlist')
    except:
        on_watchlist = False
        print('Not on watchlist')


    #testing

    #watchlist.remove(str(auction_id))
    #watchlist = ",".join(watchlist)


    #check if signed in user is the auction owner
    if auction.owner == request.user:
        is_owner = True

    if auction.is_open==False:
        winner = Bid.objects.get(item=auction).created_by
        if winner == request.user:
            message = "This auction has been closed. You've won!"
        else:
            message = f"This auction has been closed. {winner} has won."

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'form_comment':

            commentForm = CommentForm(request.POST)
            if commentForm and commentForm.is_valid():
                message = "Comment saved."
                Comment.objects.create(
                    user=request.user, auction=auction, comment=request.POST.get('comment')
                )
                return render(request, "auctions/auction.html", {
                    "auction": auction,
                    "comments": Comment.objects.filter(auction=auction),
                    "message": message,
                    "commentform": CommentForm(),
                    "is_owner": is_owner,
                    "bidform": BidForm(),
                    "current_bid": bidamount,
                    "on_watchlist": on_watchlist
                })
        elif form_type == 'form_close':
            closeForm = CloseForm(request.POST)
            if closeForm.is_valid():
                auction.is_open = False
                auction.save()
                message = "This auction has been closed."
                return render(request, 'auctions/auction.html', {
                    "auction": auction,
                    "comments": Comment.objects.filter(auction=auction),
                    "message": message,
                    "commentform": CommentForm(),
                    "is_owner": is_owner,
                    "bidform": BidForm(),
                    "current_bid": bidamount,
                    "on_watchlist": on_watchlist
                })
        elif form_type == 'form_bid':
            bidForm = BidForm(request.POST)
            if bidForm and bidForm.is_valid():
                submitted_bid = int(request.POST.get('amount'))
                if submitted_bid <= auction.starting_bid:
                    message = 'Error: Your bid must be higher than the starting bid.'
                    return render(request, 'auctions/auction.html', {
                        "auction": auction,
                        "comments": Comment.objects.filter(auction=auction),
                        "message": message,
                        "commentform": CommentForm(),
                        "is_owner": is_owner,
                        "bidform": BidForm(),
                        "current_bid": bidamount,
                        "on_watchlist": on_watchlist
                    })
                elif submitted_bid <= bid.amount:
                    message = 'Error: Your bid must be higher than the current bid.'
                    return render(request, 'auctions/auction.html', {
                        "auction": auction,
                        "comments": Comment.objects.filter(auction=auction),
                        "message": message,
                        "commentform": CommentForm(),
                        "is_owner": is_owner,
                        "bidform": BidForm(),
                        "current_bid": bidamount,
                        "on_watchlist": on_watchlist
                    })
                else:
                    bid.amount = submitted_bid
                    bid.save()
                    message = 'Bid posted successfully.'
                    bidamount = bid.amount
                    return render(request, 'auctions/auction.html', {
                        "auction": auction,
                        "comments": Comment.objects.filter(auction=auction),
                        "message": message,
                        "commentform": CommentForm(),
                        "is_owner": is_owner,
                        "bidform": BidForm(),
                        "current_bid": bidamount,
                        "on_watchlist": on_watchlist
                    })

    else:
        commentForm = CommentForm()

    return render(request, "auctions/auction.html", {
        "auction": auction,
        "comments": Comment.objects.filter(auction=auction),
        "commentform": commentForm,
        "message": message,
        "is_owner": is_owner,
        "bidform": BidForm(),
        "current_bid": bidamount,
        "on_watchlist": on_watchlist
    })

@login_required
def create(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'form_auction':
            auctionForm = AuctionForm(request.POST)
            if auctionForm and auctionForm.is_valid():
                message = "Auction created"
                Auction.objects.create(
                    owner = request.user, starting_bid = request.POST.get('starting_bid'), title = request.POST.get('title'),
                    description = request.POST.get('description'), category = Category.objects.get(pk=request.POST.get('category')),
                    image = request.POST.get('image')
                )
                auction = get_object_or_404(Auction, title=request.POST.get('title'), owner=request.user)

                Bid.objects.create(amount = request.POST.get('starting_bid'), item = auction, created_by = request.user)

                bid = Bid.objects.get(item=auction)
                bidamount = bid.amount

                return HttpResponseRedirect(auction.get_absolute_url())

                #return render(request, "auctions/auction.html", {
                #    "auction": auction,
                #    "comments": Comment.objects.filter(auction=auction),
                #    "commentform": CommentForm(),
                #    "message": message,
                #    "is_owner": True,
                #    "bidform": BidForm(),
                #    "current_bid": bidamount

                #})
    else:
        return render(request, "auctions/create.html", {
            "auctionform": AuctionForm(),
            "message": "Please enter the information for your auction:"
        })