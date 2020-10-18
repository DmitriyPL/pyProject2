from db_tables import Booking, Request


def booking_record(db, teacher, client_data):
    record = Booking(
        day=client_data['day'].view,
        time=client_data['time'].time,
        name=client_data['name'],
        phone=client_data['phone'],
        teacher_id=teacher.id
    )

    db.session.add(record)
    teacher.bookings.append(record)

    time = client_data['time']
    time.is_free = False
    db.session.add(time)


def request_record(db, request_data):

    record = Request(
        goal=request_data['goal'].goal,
        time=request_data['time'],
        name=request_data['name'],
        phone=request_data['phone']
    )

    db.session.add(record)
