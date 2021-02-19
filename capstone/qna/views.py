from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from qna.models import Board
from qna.forms import WriteForm
from django.views import generic
from django.db.models import Q


rowsPerPage = 5 # 한 페이지에 보여줄 게시물 수
def main(request):
    return HttpResponseRedirect(reverse('qna:pageview', args=(1,))) # pageview로 인수(page)에 1을 넣어 넘겨줌

def pageview(request, page): 
    current_page = page # 페이지 번호
    # 화면에 띄울 게시물 (한 페이지에 보여줄 게시물 수) 
    boardList = Board.objects.order_by('-id')[rowsPerPage * (current_page-1):rowsPerPage * current_page]
    totalCnt = Board.objects.all().count() # 총 게시물수

    pagingHelperlns = pagingHelper() # 클래스 선언
    totalPageList = pagingHelperlns.getTotalPageList(totalCnt, rowsPerPage) # 총 게시물수와 한페이지당 보여줄 게시물수에 따라 페이지수를 결정함
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
        title = request.POST['title']
        author = request.POST['author']
        content = request.POST['content']
        image = request.FILES.get('image')
        password = request.POST['password']
        
        new_post = Board.objects.create(
            title = title,
            author = author,
            content = content,
            image = image,
            password = password
        )
        new_post.save()
            
        return HttpResponseRedirect(reverse('qna:main'))




def detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.hits += 1
    board.save()

    return render(request, 'qna/detail.html', {'board':board})

def delete(request, board_id):
    if request.method == 'POST':

        board = get_object_or_404(Board, id=board_id)
        if board.password == request.POST['password']:
            board.delete()
            return HttpResponseRedirect(reverse('qna:main'))
        else:
            return render(request, 'qna/detail.html', {'board':board, 'error_message': "비밀번호 오류"})
    
    elif request.method == 'GET':
        return HttpResponseRedirect(reverse('qna:datail', args = (board_id,)))
        
    

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