// 도서관 관련 mock 데이터
export const libraries = [
  {
    id: 1,
    name: '중앙도서관',
    address: '서울특별시 강남구 테헤란로 123',
    tel: '02-1234-5678',
    operatingHours: '09:00 - 18:00',
    coordinates: {
      lat: 37.5012,
      lng: 127.0396
    },
    books: [1, 2], // 보유 도서 ID
    distance: 0.5, // km
    currentVisitors: 150,
    maxCapacity: 300
  },
  {
    id: 2,
    name: '디지털도서관',
    address: '서울특별시 강남구 역삼로 456',
    tel: '02-2345-6789',
    operatingHours: '09:00 - 21:00',
    coordinates: {
      lat: 37.4982,
      lng: 127.0421
    },
    books: [2],
    distance: 1.2,
    currentVisitors: 80,
    maxCapacity: 200
  },
  {
    id: 3,
    name: '구립도서관',
    address: '서울특별시 강남구 선릉로 789',
    tel: '02-3456-7890',
    operatingHours: '09:00 - 20:00',
    coordinates: {
      lat: 37.5042,
      lng: 127.0451
    },
    books: [1],
    distance: 1.8,
    currentVisitors: 120,
    maxCapacity: 250
  }
];
