// 사용자 관련 mock 데이터
export const users = [
  {
    id: 1,
    username: '사용자1',
    email: 'user1@example.com',
    profile_image: 'https://via.placeholder.com/50',
    favorite_books: [1, 2],
    reviews: [1],
    interests: ['소설', '에세이'],
    threads: [1],
    following: [2, 3],
    followers: [2],
    created_at: '2025-01-01T00:00:00',
    comments: [
      { id: 1, thread_id: 2, content: '좋은 글이네요!', created_at: '2025-05-20T10:00:00' }
    ]
  },
  {
    id: 2,
    username: '사용자2',
    email: 'user2@example.com',
    profile_image: 'https://via.placeholder.com/50',
    favorite_books: [2],
    reviews: [2],
    interests: ['경제/경영', '자기계발'],
    threads: [2],
    following: [1],
    followers: [1, 3],
    created_at: '2025-01-02T00:00:00',
    comments: []
  }
];
