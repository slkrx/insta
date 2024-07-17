import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

function PostHeader(props) {
  const {
    ownerShowUrl, ownerImgUrl, owner, postShowUrl, age,
  } = props;
  return (
    <div className="header p-3 d-flex align-items-center">
      <a href={ownerShowUrl} class="me-2">
        <img
          className="avatar"
          src={ownerImgUrl}
          alt=""
          width="70rem"
        />
      </a>
      <a href={ownerShowUrl} class="mx-2">
        {owner}
      </a>
      •
      <a href={postShowUrl} class="ms-2">
        {moment.duration(moment.utc(age).diff(moment(new Date()))).humanize(true)}
      </a>
    </div>
  );
}

PostHeader.propTypes = {
  ownerShowUrl: PropTypes.string.isRequired,
  ownerImgUrl: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  postShowUrl: PropTypes.string.isRequired,
  age: PropTypes.string.isRequired,
};

export default PostHeader;
