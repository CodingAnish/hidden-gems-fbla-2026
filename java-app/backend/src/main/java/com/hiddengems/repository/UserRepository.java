package com.hiddengems.repository;

import com.hiddengems.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);
    Optional<User> findByUsername(String username);

    @Query("SELECT u FROM User u WHERE u.email = :login OR u.username = :login")
    Optional<User> findByEmailOrUsername(@Param("login") String login);

    boolean existsByEmail(String email);
    boolean existsByUsername(String username);
}
