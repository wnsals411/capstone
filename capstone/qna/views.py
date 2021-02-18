from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from qna.models import Board
from qna.forms import WriteForm
from django.views import generic
from django.db.models import Q

# 한 페이지에 보여줄 게시물 수
rowsPerPage = 5
def main(request):
    current_page = 1
    # 글 번호 최신순으로 rowsPerPage 개씩 보여줌
    boardList = Board.objects.order_by('-id')[rowsPerPage * (current_page-1):rowsPerPage * current_page]
    # 총 게시물 수
    totalCnt = Board.objects.all().count() 

    pagingHelperlns = pagingHelper()
    totalPageList = pagingHelperlns.getTotalPageList(totalCnt, rowsPerPage)
    print ('totalPageList', totalPageList)
    return render(request, 'qna/main.html', {'boardList': boardList, 'totalCnt': totalCnt, 
                                            'current_page': current_page, 'totalPageList': totalPageList})


class pagingHelper:
    def getTotalPageList(self, total_cnt, rowsPerPage):
        if ((total_cnt % rowsPerPage) == 0):
            self.total_pages = int(total_cnt / rowsPerPage)
            print ('getTotalPage #1')
        else:
            self.total_pages = int((total_cnt / rowsPerPage) + 1)
            print ('getTotalPage #2')
        
        self.totalPageList = []
        for j in range(self.total_pages):
            self.totalPageList.append(j + 1)

        return self.totalPageList
    
    def __init__(self):
        self.total_pages = 0
        self.totalPageList = 0


def write(request): # 글 쓰기
    if request.method == 'GET':
        form = WriteForm()

        return render(request, 'qna/write.html', {'form': form})
    if request.method == 'POST':
        form = WriteForm(request.POST)

        if form.is_valid():
            form.save()
            
        return HttpResponseRedirect(reverse('qna:main'))

def pageview(request, page): # 페이지 번호
    current_page = page
    boardList = Board.objects.order_by('-id')[rowsPerPage * (current_page-1):rowsPerPage * current_page]
    totalCnt = Board.objects.all().count() 

    pagingHelperlns = pagingHelper()
    totalPageList = pagingHelperlns.getTotalPageList(totalCnt, rowsPerPage)
    print ('totalPageList', totalPageList)
    return render(request, 'qna/main.html', {'boardList': boardList, 'totalCnt': totalCnt, 
                                            'current_page': current_page, 'totalPageList': totalPageList})


def detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    
    board.hits += 1
    board.save()

    return render(request, 'qna/detail.html', {'board':board})

def delete(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    
    board.delete()
    
    return HttpResponseRedirect(reverse('qna:main'))

def search(request):
    if request.method == 'POST':
        searchWord = request.POST['searchStr']
        board_list = Board.objects.filter(Q(title__icontains=searchWord) | Q(content__icontains=searchWord) | Q(author__icontains=searchWord)).distinct().order_by('-create_at')
        totalCnt = board_list.count()
        pagingHelperlns = pagingHelper()
        totalPageList = pagingHelperlns.getTotalPageList(totalCnt, rowsPerPage)

        return render(request, 'qna/main.html', {'boardList': board_list, 'totalCnt': totalCnt, 
                                            'current_page': 1, 'totalPageList': totalPageList})
                                            
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('qna:main'))
                                