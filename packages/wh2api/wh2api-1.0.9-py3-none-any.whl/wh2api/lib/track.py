# -*- coding: utf-8 -*-

from . import wh_setting, api_list

#WH2API - track.md

#1. 트랙 버전 목록 조회
def version(project_idx,from_date="yy-mm-dd",to_date="yy-mm-dd",last=""):
    '''
    :param project_idx:프로젝트 index
    :param from_date: 시작일정
    :param to_date: 종료일정
    :param last: 마지막 버전만 확인하고 싶을땐 "last"입력
    :return:
    '''
    #last = "" or "last"

    api = api_list.track_version %(project_idx,from_date,to_date,last)
    result = wh_setting.get_requests(api=api)
    return result

def shot_task(project_idx,episode_idx,sequence_idx="all",page=1):
    '''
    :param project_idx:프로젝트 인덱스
    :param episode_idx: 에피소드 인덱스
    :param sequence_idx: 필요시 인덱스 입력
    :param page: 기본값 1페이지
        {'next_data': False, 'page': 2 }으로 다음페이지여부가 표시됨
    :return:
    '''

    api = api_list.track_shot_task_list %(project_idx,episode_idx,sequence_idx)
    data = {'page':page}

    result = wh_setting.get_requests(api=api,data=data)
    return result

def asset_task(project_idx,category_idx='all',page=1):
    '''

    :param project_idx: 프로젝트 인덱스
    :param category_idx: 필요시 카테고리 인덱스 입력
    :param page: 기본값1페이지
        {'next_data': False, 'page': 2 }으로 다음페이지여부가 표시됨
    :return:
    '''

    api = api_list.track_asset_task_list %(project_idx,category_idx)
    data ={'page':page}

    result = wh_setting.get_requests(api=api,data=data)
    return result