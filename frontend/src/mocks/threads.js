// 쓰레드 관련 mock 데이터
export const threads = [
  {
    id: 1,
    title: '어린 왕자를 읽고',
    content: '어린 왕자는 진정한 사랑과 책임에 대해 이야기하는 책입니다...',
    bookId: 1,
    bookTitle: '어린 왕자',
    author: {
      id: 1,
      username: '사용자1',
      profile_image: 'https://via.placeholder.com/50'
    },
    createdAt: '2025-05-23T10:00:00',
    likes: 15,
    comments: [
      {
        id: 1,
        content: '좋은 리뷰네요!',
        author: {
          id: 2,
          username: '사용자2',
          profile_image: 'https://via.placeholder.com/50'
        },
        createdAt: '2025-05-23T10:30:00',
        likes: 3,
        replies: [
          {
            id: 2,
            content: '감사합니다 :)',
            author: {
              id: 1,
              username: '사용자1',
              profile_image: 'https://via.placeholder.com/50'
            },
            createdAt: '2025-05-23T11:00:00',
            likes: 1
          }
        ]
      }
    ],
    tags: ['소설', '고전'],
    rating: 5,
    aiGenerated: {
      feedback: '이 리뷰는 매우 통찰력 있게 작성되었습니다...',
      image: 'https://via.placeholder.com/300'
    }
  },
  {
    id: 2,
    title: '데미안 독후감',
    content: '데미안은 자아를 찾아가는 여정을 담은 소설입니다...',
    bookId: 2,
    bookTitle: '데미안',
    author: {
      id: 2,
      username: '사용자2',
      profile_image: 'https://via.placeholder.com/50'
    },
    createdAt: '2025-05-22T15:00:00',
    likes: 10,
    comments: [],
    tags: ['소설', '성장'],
    rating: 4.5,
    aiGenerated: {
      feedback: '이 리뷰는 작품의 핵심 주제를 잘 파악했습니다...',
      image: 'https://via.placeholder.com/300'
    }
  }
];
