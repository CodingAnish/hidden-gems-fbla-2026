package com.hiddengems.repository;

import com.hiddengems.entity.Favorite;
import com.hiddengems.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FavoriteRepository extends JpaRepository<Favorite, Long> {

    List<Favorite> findByUserOrderByCreatedAtDesc(User user);
    Optional<Favorite> findByUserIdAndBusinessId(Long userId, Long businessId);
    boolean existsByUserIdAndBusinessId(Long userId, Long businessId);
    void deleteByUserIdAndBusinessId(Long userId, Long businessId);
}
