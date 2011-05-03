# -*- encoding: utf-8 -*-

# Signal after syncdb
from openkala.quarter.models import *

def after_syncdb(sender, **kwargs):

    """
    THIS IS DUMMY CONTENT CODE
    """

    # StandardHeader
    standard_header1, created = StandardHeader.objects.get_or_create(title='วิทยาศาสตร์')
    standard_header2, created = StandardHeader.objects.get_or_create(title='สังคมศึกษา ศาสนา และวัฒนธรรม')
    standard_header3, created = StandardHeader.objects.get_or_create(title='การงานอาชีพและเทคโนโลยี')
    standard_header4, created = StandardHeader.objects.get_or_create(title='สุขศึกษาและพลานามัย')
    
    standard_header5, created = StandardHeader.objects.get_or_create(title='ร่างกาย')
    standard_header6, created = StandardHeader.objects.get_or_create(title='อารมณ์ - จิตใจ สังคม')
    standard_header7, created = StandardHeader.objects.get_or_create(title='สติปัญญา')

    # Project
    project1, created = Project.objects.get_or_create(
        name='ผ้า', 
        grade=3, 
        year=2008, 
        quarter=1, 
        standard_header1=standard_header1, 
        standard_header2=standard_header2, 
        standard_header3=standard_header3, 
        standard_header4=standard_header4
    )

    project2, created = Project.objects.get_or_create(
        name='ผ้ ไผ่ไหวเอน', 
        grade=0, 
        year=2003, 
        quarter=4, 
        standard_header1=standard_header5, 
        standard_header2=standard_header6, 
        standard_header3=standard_header7
    )

    # Topic
    topic1, created = Topic.objects.get_or_created(
        title='1. ผ้าคืออะไร', 
        body='1.1 ความหมายและความสำคัญ <br /> 1.2 วิวัฒนาการ', 
        project=project1,
        standars1='ว 2.1: เข้าใจว่าเสื้อผ้าเครื่องนุ่งห่ม เป็นปัจจัยสำคัญ <br /> ว 2.2: เข้าใจสิ่งแวดล้อมท้องถิ่น',
        standars2='ส 2.1: อธิบายเกี่ยวกับวิวัฒนาการของผ้า <br /> ส 3.1: อธิบายได้ว่าทรัพยากรธรรมชาติที่มีอยู่อย่างจำกัด',
        standars3='ง 1.1: เข้าใจการทำงาน มีความคิดสร้างสรรค์ <br /> ง 3.1: เข้าใจธรรมชาติในท้องถิ่น',
        standars4='พ 1.1: เข้าใจธรรมชาติของการเจริญเติบโตและพัฒนาการของมนุษย์'
    )
    topic2, created = Topic.objects.get_or_created(
        title='2. ทำอย่างไรให้เสื้อผ้าสะอาดและสวยงาม', 
        body='2.1 การเลือกใช้เสื้อผ้า <br /> 2.2 การตัดเย็บผ้า', 
        project=project1,
        standars1='ว 1.2: อธิบายความแตกต่างของบุคคล แต่ละรูปร่าง เชื้อชาติ ประเทศ <br /> ว 2.1: อธิบายความสัมพันธ์ของแต่ละท้องถิ่น',
        standars2='ส 2.1: เข้าใจในประเพณีวัฒนธรรมของท้องถิ่น <br /> ส 4.2: อธิบายได้ว่าทรัพยากรธรรมชาติที่มีอยู่อย่างจำกัด',
        standars3='ง 1.5: ศึกษาสัญชาตญาณดิบในที่มืด เข้าใจการทำงาน มีความคิดสร้างสรรค์ <br /> ง 6.1: เข้าใจหนอนดักแด และเข้าใจธรรมชาติในท้องถิ่น',
        standars4='พ 3.1: กฎการ เกิด แก่ เจ็บ ตาย และเข้าใจธรรมชาติของการเจริญเติบโตและพัฒนาการของมนุษย์'
    )

    # Plan
    # TODO: Add detail
    plan1, created = Plan.objects.get_or_created(
        week=1,
        goal='',
        activity='',
        sub_topic='',
        key_thinking='',
        performance='',
        topic=topic1
    )

    plan2, created = Plan.objects.get_or_created(
        week=2,
        goal='',
        activity='',
        sub_topic='',
        key_thinking='',
        performance='',
        topic=topic2
    )

    # Task
    # TODO: Add detail
    task1, created = Task.objects.get_or_created(
        day=1,
        hour=2,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan1
    )
    task2, created = Task.objects.get_or_created(
        day=2,
        hour=1,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan1
    )
    task3, created = Task.objects.get_or_created(
        day=3,
        hour=1,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan1
    )
    task4, created = Task.objects.get_or_created(
        day=4,
        hour=1,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan1
    )
    task5, created = Task.objects.get_or_created(
        day=5,
        hour=2,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan1
    )

    task6, created = Task.objects.get_or_created(
        day=1,
        hour=2,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan2
    )
    task7, created = Task.objects.get_or_created(
        day=2,
        hour=1,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan2
    )
    task8, created = Task.objects.get_or_created(
        day=3,
        hour=1,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan2
    )
    task9, created = Task.objects.get_or_created(
        day=4,
        hour=1,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan2
    )
    task10, created = Task.objects.get_or_created(
        day=5,
        hour=2,
        activity='',
        source='',
        work='',
        assessment= '',
        plan=plan2
    )

from django.db.models.signals import post_syncdb
post_syncdb.connect(after_syncdb, dispatch_uid="openkala.quarter.management")
