// 도서 관련 mock 데이터
export const books = [
  {
    id: 1,
    title: '책 제목 1',
    author: '저자 1',
    description: '책 설명 1',
    cover_image: 'https://via.placeholder.com/150',
    rating: 4.5,
    category: '소설',
    reviews: [
      { id: 1, user: '사용자1', content: '리뷰 내용 1', rating: 4 },
      { id: 2, user: '사용자2', content: '리뷰 내용 2', rating: 5 }
    ]
  },
  {
    id: 2,
    title: '책 제목 2',
    author: '저자 2',
    description: '책 설명 2',
    cover_image: 'https://via.placeholder.com/150',
    rating: 4.0,
    category: '에세이',
    reviews: [
      { id: 3, user: '사용자3', content: '리뷰 내용 3', rating: 4 }
    ]
  }
];
