from eventflow import EventBus

# Database
patients = {
  "1": {
    "name": "Charles A. Schneider",
    "email": "CharlesASchneider@gmail.com",
    "birthday": "April 14, 1992"
  },
  "2": {
    "name": "Donna M. Holmes",
    "email": "DonnaMHolmes@gmail.com",
    "birthday": "October 13, 1981"
  }
}

def create_medical_record(event):
  patient = patients[event["data"]["patient_id"]]
  print("New medical record created for {}".format(patient["name"]))

#############################
#       Test functions      #
#############################

def test_add_listener(bus: EventBus):
  assert len(bus) == 0
  bus.add_listener(event_type="new:patient", listener=create_medical_record)
  assert len(bus) > 0

  bus.remove_listener(event_type="new:patient", listener=create_medical_record)


def test_remove_listener(bus: EventBus):
  bus.add_listener(event_type="new:patient", listener=create_medical_record)
  
  assert len(bus) > 0
  bus.remove_listener(event_type="new:patient", listener=create_medical_record)
  assert len(bus) == 0


def test_len(bus: EventBus):
  bus.add_listener(event_type="new:patient", listener=create_medical_record)
  assert len(bus) > 0
  bus.remove_listener(event_type="new:patient", listener=create_medical_record)
  assert len(bus) == 0


def test_fire(bus: EventBus):
  bus.add_listener(event_type="new:patient", listener=create_medical_record)
  bus.fire(event_type="new:patient", data={"patient_id": "1"})
  bus.remove_listener(event_type="new:patient", listener=create_medical_record)


def test_listen(bus: EventBus):
  @bus.listen(event_type="test")
  def func(event):
    assert event["data"]["message"] == "Hello world!"

  bus.fire(event_type="test", data={"message": "Hello world!"})


def test_listeners(bus: EventBus):
  assert bus.listeners == {}
  bus.add_listener(event_type="new:patient", listener=create_medical_record)
  assert bus.listeners != {}

  print(bus.listeners)
  bus.remove_listener(event_type="new:patient", listener=create_medical_record)
  